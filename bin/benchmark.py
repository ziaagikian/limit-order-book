import threading
import random
import time

from queues.queueType import QueueType
from database.mongoHelper import MongoHelper
from queues.workerQueue import WorkerQueue
from lib.src.order import Order
from lib.src.orderBook import OrderBook
from lib.utils.commons import *

exitFlag = 0


class QueueThread(threading.Thread):
    def __init__(self, tid, name, queue):
        threading.Thread.__init__(self)
        self.daemon = True
        self.id = tid
        self.name = name
        self.queue = queue

    def run(self) -> None:
        print("Starting " + self.name)
        process_data(self.queue)
        print("Exiting " + self.name)


def process_data(queue):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = queue.get()
            if queue.type == QueueType.HISTORY_QUEUE:
                dbOps.insertDocuments(dbOps.order_coll, data)
            else:
                dbOps.insertDocuments(dbOps.transaction_col, data)
            queue.task_done()
            queueLock.release()
            # sys.stdout.write("{} processing \n".format(name))
        else:
            queueLock.release()


def direct_benchmark(num_order):
    order_book = OrderBook()
    orders = order_list(num_order)
    tic = time.time()
    len_orders = len(orders)
    for ctr in range(len_orders):
        order_book.execute_order(orders[ctr])
    toc = time.time()
    total = toc - tic
    print_benchmark(num_order, total)


def database_benchmark(num_ord, hist_batch_size, trans_batch_size):
    orders = order_list(num_ord)
    history_batch = []
    transaction_batch = []

    order_dbbook = OrderBook()
    len_orders = len(orders)
    tic = time.time()
    for ctr in range(len_orders):
        order = orders[ctr]
        transactions = order_dbbook.execute_order(order)
        if len(transactions) > 0:
            transaction_batch.extend(transactions.executionsJson)

        if ctr < (num_ord - 1):
            # Batching for the transactions
            if len(transaction_batch) == trans_batch_size:
                queueLock.acquire()
                workQueue.type = QueueType.TRANSACTIONS_QUEUE
                workQueue.put(transaction_batch)
                transaction_batch = []
                queueLock.release()
        else:
            # Insert Remaining transactions
            if len(transaction_batch) > 0:
                queueLock.acquire()
                workQueue.type = QueueType.TRANSACTIONS_QUEUE
                workQueue.put(transaction_batch)
                queueLock.release()

        history_batch.append(order.json_string(unique_id=True))

        if len(history_batch) == hist_batch_size:
            queueLock.acquire()
            workQueue.type = QueueType.HISTORY_QUEUE
            workQueue.put(history_batch)
            # Clear Batch List
            history_batch = []
            queueLock.release()
    toc = time.time()
    total = toc - tic

    print_benchmark(num_ord, total)


def order_list(num_order):
    starting_price = 1
    starting_qty = 10
    order_id = 0
    random.seed(13)
    orders = []
    for _ in range(num_order):
        order_id += 1
        order_type = random.choice(["B", "S"])
        order_price = random.randint(starting_price, num_order * 100)
        order_qty = random.randint(starting_qty, num_order * 1000)
        orders.append(Order(order_id, order_type, order_price, order_qty))
    return orders


if __name__ == "__main__":
    # Benchmark Trade Matching Engine
    direct_benchmark(100000)
    # Benchmarking Database and Matching Engine
    queueLock = threading.Lock()
    # 1000
    batch_size = 10000
    qThreadID = 1
    threads = []
    num_threads = 2
    workQueue = WorkerQueue(QueueType.HISTORY_QUEUE, batch_size)

    for i in range(num_threads):
        tName = "Thread-" + str(qThreadID)
        thread = QueueThread(qThreadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        qThreadID += 1
    dbOps = MongoHelper()
    # print(dbOps)
    dbOps.createDB()
    # Clearing Database Entries
    dbOps.clearCollections()

    dbOps.createCollections()
    #
    database_benchmark(100000, batch_size, 100)

    while not workQueue.empty():
        pass
    exitFlag = 1
    for t in threads:
        t.join()
    # Clearing Dummy Database Entries
    dbOps.clearCollections()
    dbOps.close()
    sys.stdout.write("Exiting Main Thread\n")
    # total = time.time() - tic
