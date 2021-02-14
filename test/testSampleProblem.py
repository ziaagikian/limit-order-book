import unittest
from lib.src.order import Order
from lib.src.orderBook import OrderBook


class TestAssignment(unittest.TestCase):
    def test_assignment(self):
        book = OrderBook()
        book.execute_order(Order(1, 'S', 23, 1000))
        book.execute_order(Order(2, 'S', 28, 500))
        book.execute_order(Order(3, 'S', 29, 750))
        book.execute_order(Order(4, 'S', 32, 1200))
        transactions = book.execute_order(Order(10, 'B', 32, 1800))
        # print(transactions.executionsJson)
        self.assertEqual(len(transactions.executionsJson), 3)

        book.print_real_time_order_book()

    if __name__ == "__main__":
        unittest.main()
