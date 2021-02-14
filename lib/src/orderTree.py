from bintrees import FastRBTree

from lib.src.limitOrder import LimitOrder
from lib.utils.transactions import Transactions


class OrderTree(object):
    """
    Tree can be sorted based on Price only. Other criteria like eventTime is not considered.
    """

    def __init__(self):
        self.tree = FastRBTree()
        # self.trades = deque()  # Index [0] is most recent trade
        # self.tree = FastBinaryTree()
        self.order_dic = {}  # {orderID, order}
        self.price_dic = {}  # {price, limit Order List}
        self.min_price = None
        self.max_price = None
        # self.transactions = Transactions()

    def __len__(self):
        return len(self.order_dic)

    def add_price(self, price):
        order = LimitOrder()
        self.tree.insert(price, order)
        self.price_dic[price] = order
        if self.max_price is None or self.max_price < price:
            self.max_price = price
        if self.min_price is None or price < self.min_price:
            self.min_price = price

    def delete_price(self, price):
        self.tree.remove(price)
        # Delete Order from Order dictionary
        for order in self.price_dic[price]:
            del self.order_dic[order.id]
            # Add order to completed Dictionary
            # self.completed_order_dic[order.id] = order
        del self.price_dic[price]
        # Update max and in min price
        if self.max_price == price:
            try:
                self.max_price = self.tree.max_key()
            except ValueError:
                self.max_price = None
        if self.min_price == price:
            try:
                self.min_price = self.tree.min_key()
            except ValueError:
                self.min_price = None

    def add_price_order(self, order):
        if order.price not in self.price_dic:
            self.add_price(order.price)
        self.price_dic[order.price].add_order(order)
        # Also keep it in the order mapping
        self.order_dic[order.id] = order

    def match_price_order(self, incoming_order):
        if len(self.price_dic) == 0:
            return []

        # Buy Order will do trade with min(sell_tree)
        # Sell Order will do trade with max(buy_tree)
        transactions = Transactions()
        feasible_price = self.min_price if incoming_order.is_buy else self.max_price
        # Loop through the tree and execute trade
        while (((incoming_order.is_buy and incoming_order.price >= feasible_price)
                or (incoming_order.is_sell and incoming_order.price <= feasible_price))
               and incoming_order.peak_quantity > 0):
            matched_orders = self.price_dic[feasible_price]
            matched_order = matched_orders.match_order(incoming_order, self.order_dic)
            # Append to Custom Lists
            transactions.executions.extend(matched_order.executions)
            transactions.executionsJson.extend(matched_order.executionsJson)
            # Delete executed price
            if matched_orders.length == 0:
                self.delete_price(feasible_price)
                if len(self.price_dic) == 0:
                    break
                feasible_price = self.min_price if incoming_order.is_buy else self.max_price

        return transactions
