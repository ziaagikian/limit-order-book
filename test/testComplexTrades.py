import unittest
from lib.src.order import Order
from lib.src.orderBook import OrderBook


class TestComplexTrades(unittest.TestCase):

    def test_MiscTrades(self):
        book = OrderBook()
        book.execute_order(Order(1, "B", 3375, 200))
        book.execute_order(Order(2, "B", 3374, 500))
        book.execute_order(Order(3, "S", 3378, 300))
        book.execute_order(Order(4, "B", 3375, 100))
        trades = book.execute_order(Order(5, "S", 3377, 200))

        # No trade
        self.assertEqual(len(trades.executionsJson), 0)
        book.print_real_time_order_book()


if __name__ == '__main__':
    unittest.main()
