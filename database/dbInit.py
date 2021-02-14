from database.mongoHelper import MongoHelper


# Test Script for Checking MongoDb setup
def main():
    helper = MongoHelper()
    print("Creating Database")
    helper.createDB()
    print("Creating Collections")
    helper.createCollections()
    print("Database script run successfully, in case of error check logs accordingly.")


if __name__ == "__main__":
    main()
