import unittest
from lib.src.order import Order
from lib.src.orderBook import OrderBook


class TestOrderBook(unittest.TestCase):

    def test_addPrice(self):
        book = OrderBook()
        #   Sample Order as given in assignment
        # 1, SELL, 23, 1000
        book.execute_order(Order(1, "S", 23, 1000))
        self.assertTrue(1, book.sell_tree.order_dic)
        self.assertTrue(23 == book.sell_tree.max_price)

    def test_multipleOrders(self):
        book = OrderBook()
        # 1, SELL, 23, 1000
        # 2, SELL, 28, 500
        order1 = Order(1, "S", 23, 1000)
        order2 = Order(2, "S", 28, 500)
        book.execute_order(order1)
        book.execute_order(order2)
        # print("MAX Price ", book.sell_tree.max_price)
        # print("MIN Price ", book.sell_tree.min_price)
        self.assertTrue(book.sell_tree.max_price == 28)
        self.assertTrue(book.sell_tree.min_price == 23)
        order3 = Order(1, "B", 24, 900)
        order4 = Order(2, "B", 18, 500)
        book.execute_order(order3)
        book.execute_order(order4)
        print("MAX Buy Price ", book.buy_tree.max_price)
        self.assertTrue(book.buy_tree.max_price == 18)
        # self.assertTrue(book.buy_tree.min_price == 18)

    if __name__ == "__main__":
        unittest.main()
