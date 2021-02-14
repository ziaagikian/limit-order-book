import unittest

from lib.src.order import Order
from lib.src.limitOrder import LimitOrder


class TestLimitOrder(unittest.TestCase):

    def test_LimitOrderAdd(self):
        iters = 1000
        limit_orders = self.fillDummyList(iters)
        self.assertTrue(limit_orders.length == iters)

    def test_test_LimitOrderDelete(self):
        """
        First create dummy Limit Orders then test deletion operation
        :return:
        """
        iters = 100
        limit_orders = self.fillDummyList(iters)

        # Test delete Tail
        limit_orders.delete_tail()
        op = 1
        self.assertTrue(limit_orders.tail.id == iters-op)
        self.assertTrue(limit_orders.length == iters-op)

        # Delete Head
        limit_orders.delete_head()
        op += 1
        self.assertTrue(limit_orders.head.id == op)
        self.assertTrue(limit_orders.length == iters-op)

        # Delete all
        ctr = iters - op
        for i in range(ctr, 0, -1):
            limit_orders.delete_head()
        self.assertTrue(limit_orders.length == 0)
        self.assertTrue(limit_orders.head is None)
        self.assertTrue(limit_orders.tail is None)

    @staticmethod
    def fillDummyList(nums):
        ord_id = 1
        ord_price = 32
        ord_qty = 1800
        limit_orders = LimitOrder()
        for i in range(nums):
            order = Order(ord_id, type, ord_price, ord_qty)
            limit_orders.add_order(order)
            ord_id += 1
        return limit_orders


if __name__ == '__main__':
    unittest.main()
