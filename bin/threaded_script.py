import time
import threading

from queues.workerQueue import WorkerQueue
from queues.queueType import QueueType
from database.mongoHelper import MongoHelper
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
            # print("%s processing " % (name, ))
        else:
            queueLock.release()


if __name__ == '__main__':

    # print("_" * 10, "Queue Demo ", "_" * 10)
    num_threads = 2
    # nameList = []
    history_batch_size = 1000
    queueLock = threading.Lock()
    # Setting Database attributes
    dbOps = MongoHelper()
    # print(dbOps)
    dbOps.createDB()
    # Clearing Dummy Database Entries
    dbOps.clearCollections()
    dbOps.createCollections()

    workQueue = WorkerQueue(QueueType.HISTORY_QUEUE, history_batch_size)
    qThreads = []
    qThreadID = 1
    history_batch = []

    # Create new threads
    for i in range(num_threads):
        tName = "Thread" + str(qThreadID)
        thread = QueueThread(qThreadID, tName, workQueue)
        thread.start()
        qThreads.append(thread)
        qThreadID += 1

    order_book = OrderBook()
    orders_executed = 0  # Order counter
    tic = time.time()
    while True:
        try:
            line = sys.stdin.readline()
            line_fields = line.split(",")

            if not line:
                sys.stderr.write("End of File.\n")
                break
            ord_type = line_fields[0]  # B or S
            ord_id = line_fields[1]
            ord_price = int(line_fields[2])
            ord_qty = int(line_fields[3])
            # workQueue.put(None)
            order = Order(ord_id, ord_type, ord_price, ord_qty)
            # queueLock.acquire(blocking=False)
            transactions = order_book.execute_order(order)
            if len(transactions) > 0:
                queueLock.acquire()
                workQueue.type = QueueType.TRANSACTIONS_QUEUE
                workQueue.put(transactions.executionsJson)
                queueLock.release()

            # sell_tree = order_book.sell_tree.tree
            history_batch.append(order.json_string(unique_id=True))
            if len(history_batch) == history_batch_size:
                queueLock.acquire()
                workQueue.type = QueueType.HISTORY_QUEUE
                workQueue.put(history_batch)
                queueLock.release()
                # Clear Batch List
                history_batch = []

        except KeyboardInterrupt:
            break

        orders_executed += 1

    # Wait for queue to empty
    while not workQueue.empty():
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in qThreads:
        t.join()
    sys.stdout.write("Exiting Main Thread\n")
    total = time.time() - tic
    dbOps.close()

    print_benchmark(orders_executed, total)
