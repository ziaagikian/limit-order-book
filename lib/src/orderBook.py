from lib.utils.treeIterator import TreeIterator
from lib.src.orderTree import OrderTree


class OrderBook(object):
    def __init__(self):
        self.buy_tree = OrderTree()
        self.sell_tree = OrderTree()

    # TODO Make this atomic
    def execute_order(self, incoming_order):
        """
        Process Sell or Buy Order
        :param incoming_order:
        :return:
        """
        matched_tree = self.buy_tree if incoming_order.is_sell else self.sell_tree
        # Order is not altered, match incoming Order with matched_tree
        transaction = matched_tree.match_price_order(incoming_order)

        if incoming_order.peak_quantity != 0:
            incoming_order.restore_peak_quantity()
            altered_tree = self.buy_tree if incoming_order.is_buy else self.sell_tree
            # print(incoming_order)
            altered_tree.add_price_order(incoming_order)

        incoming_order.transaction_quantity = 0
        # self.print_real_time_order_book()

        return transaction

    def cancel_order(self, order_id):
        pass

    def change_order(self, order_id, modified_order):
        pass

    def print_real_time_order_book(self):
        buy_iter = TreeIterator(self.buy_tree.tree.values(reverse=True))
        sell_iter = TreeIterator(self.sell_tree.tree.values())

        print()
        self.print_line()
        print("|======= Order Book Status after Incoming Order ====================|")
        self.print_line()
        print("|  Id     |   Type     |       Qty   | Price   |    Status          |")
        self.print_line()

        while sell_iter.hasnext():
            print("|", end="")
            next(sell_iter).print_order()
            print("|")

        while buy_iter.hasnext():
            print("|", end="")
            next(buy_iter).print_order()
            print("|")

        self.print_line()

    @staticmethod
    def print_line():
        print("|" + "-" * 67 + "|")
