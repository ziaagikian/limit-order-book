import sys
from pymongo import MongoClient
from pymongo.errors import OperationFailure, DuplicateKeyError, BulkWriteError
from database.settings import DatabaseConfig as config


class MongoHelper:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URL,
                                  serverSelectionTimeoutMS=config.TIME_OUT, maxPoolSize=config.MAX_POOLING)
        try:
            self.dbList = self.client.list_database_names()
            sys.stdout.write("DataBase Connection Established........\n")
        except OperationFailure as error:
            self.errorAndExit(error)

        self.db = None
        self.order_coll = None
        self.transaction_col = None

    def createDB(self):
        # if config.DATABASE_NAME not in self.dbList:
        try:
            self.db = self.client[config.DATABASE_NAME]
            sys.stdout.write("DataBase Table {} created.\n".format(config.DATABASE_NAME))
        except OperationFailure as error:
            self.errorAndExit(error)

    def createCollections(self):
        # collist = self.db.list_collection_names()
        self.order_coll = self.db[config.ORDER_BOOK_COL]
        # if config.HISTORY_COL not in collist:
        self.transaction_col = self.db[config.TRANSACTION_COL]

    def close(self):
        sys.stdout.write("Closing Database Connection!\n")
        self.client.close()

    @staticmethod
    def insertDocuments(collection, data: list):  # -> Any:
        # if data instance of list
        if collection is None:
            raise AttributeError
        if len(data) == 1:
            try:
                entry = collection.insert_one(data[0])
                return entry.inserted_id
            except DuplicateKeyError as error:
                sys.stderr.write("Duplicate Key Error: {}\n".format(error))
                return None

        elif len(data) > 1:
            try:
                entries = collection.insert_many(data)
                # print("ZEEE 2", entry_ids.inserted_ids)
                return entries.inserted_ids
            except DuplicateKeyError as error:
                sys.stderr.write("Duplicate Key Error: {}\n".format(error))
                return None
            # Can occure during Multiple Benchmarking, in real life Order ID will be
            # unique. In Simulated environment can be ignored.
            except BulkWriteError as blk_error:
                sys.stderr.write("Bulk Error because of Duplication: {}\n".format(blk_error))
                sys.stdout.write("Clear Collection and Proceed.\n")
                return None
        else:
            sys.stdout.write("Data is not valid.\n")

    def clearCollections(self):
        sys.stdout.write("Clearing dummy entries from database.\n")
        self.db[config.ORDER_BOOK_COL].drop()
        self.db[config.TRANSACTION_COL].drop()

    @staticmethod
    def limitResult(collection, query, limit):
        res = collection.find(query).limit(limit)
        return res

    @staticmethod
    def updateManyDocs(col, query, new_vals):
        # query = { "name": { "$regex": "^Z" } } # Name starting from Z
        # new_vals = { "$set": { "name": "Minnie" } } # Set new Name
        cnt = col.update_many(query, new_vals)
        print(cnt.modified_count, "documents updated.")

    @staticmethod
    def updateDoc(col, query, new_vals):
        # query = {"address": "Valley 345"}
        # new_vals = {"$set": {"address": "Canyon 123"}}
        col.update_one(query, new_vals)

    @staticmethod
    def errorAndExit(error):
        sys.stderr.write("Data Base Connection failed. Error: {}\n".format(error))
        sys.stderr.write("Program exiting check you connection and try again!\n")
        sys.exit(-1)
