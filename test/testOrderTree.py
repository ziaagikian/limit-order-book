import unittest
from lib.src.order import Order
from lib.src.orderTree import OrderTree


class TestOrderTee(unittest.TestCase):

    def test_OrderTeeAddPrice(self):
        nodes = 10
        tree = self.fillDummyTree(nodes)
        self.assertTrue(len(tree.price_dic) == nodes)
        self.assertTrue(tree.max_price == nodes - 1)

    def test_OrderTreeDeletePrice(self):
        tree = OrderTree()
        tree.add_price_order(Order(1, "B", 700, 8900))
        tree.add_price_order(Order(2, "B", 900, 890))
        tree.add_price_order(Order(3, "S", 700, 899))
        tree.add_price_order(Order(4, "B", 700, 8900))

        self.assertTrue(len(tree.price_dic) == 2)
        self.assertTrue(len(tree.order_dic) == 4)
        # print(tree.order_dic)
        # print(tree.price_dic)
        tree.delete_price(700)
        # print(tree.order_dic.__len__() )
        self.assertTrue(len(tree.price_dic) == 1)
        self.assertTrue(len(tree.order_dic) == 1)
        # Delete the rest
        tree.delete_price(900)
        self.assertTrue(len(tree.price_dic) == 0)
        self.assertTrue(len(tree.order_dic) == 0)

    @staticmethod
    def fillDummyTree(num_nodes):
        p_tree = OrderTree()
        price = 0  # dummy price
        for ctr in range(num_nodes):
            p_tree.add_price(price + ctr)
        return p_tree


if __name__ == "__main__":
    unittest.main()
