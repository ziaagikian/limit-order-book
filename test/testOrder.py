import unittest
from lib.src.order import Order


class TestOrder(unittest.TestCase):
    def test_limitSingleOrder(self):
        """
        1 Sell 23 1000
        Test Orders given in Assignment
        """
        ord_id = 1
        ord_type = "S"
        ord_price = 23
        ord_qty = 1000
        order = Order(ord_id, ord_type, ord_price, ord_qty)
        self.assertTrue(order.is_sell)
        self.assertFalse(order.is_buy)
        self.assertEqual(order.type, ord_type)
        self.assertEqual(order.price, ord_price)
        self.assertEqual(order.quantity, ord_qty)

    def test_doTrade(self):
        ord_type = 'S'
        ord_id = 100345
        ord_price = 5103
        ord_qty = 100000
        trade = 5000
        # order_peak = 10000
        order = Order(ord_id, ord_type, ord_price, ord_qty)
        order.do_trade(trade)
        # print(order.peak_quantity)
        # print(order.transaction_quantity)
        self.assertTrue(order.transaction_quantity == trade)
        self.assertTrue(order.peak_quantity == 95000)

    if __name__ == "__main__":
        unittest.main()
