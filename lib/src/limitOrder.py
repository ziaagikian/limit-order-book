from lib.utils.transactions import Transactions


class LimitOrder(object):
    """
    Composition class to main doubly linkedlist for Order class.
    This is the basic datastructure for limit order. Orders are added/removed
    in doubly linkedlist ensuring FIFO i-e start from head i-e adding to tail.
    """
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0
        self.visited = False
        self.iter_temp = None

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, h2):
        self._head = h2

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, t2):
        self._tail = t2

    @property
    def length(self):
        return self._length

    def add_order(self, order):
        # First element
        if self.head is None:
            order.nxt = None
            order.prev = None
            self.head = order
            self.tail = order
        # Add to tail
        else:
            order.prev = self.tail
            order.nxt = None
            self.tail.nxt = order
            self.tail = order

        self._length += 1

    def delete_head(self):
        self.delete_order(self.head)

    def delete_tail(self):
        self.delete_order(self.tail)

    def delete_order(self, order):
        """
        Given Order will present in list
        :param order:
        :return:
        """
        self._length -= 1
        # Remove last element
        if self.length == 0:
            self.head = None
            self.tail = None

        next_order = order.nxt
        prev_order = order.prev
        # Delete from the middle of linked list
        if next_order is not None and prev_order is not None:
            next_order.prev = prev_order
            prev_order.nxt = next_order
        # Delete head
        elif next_order is not None:
            next_order.prev = None
            self.head = next_order
        # Delete tail
        elif prev_order is not None:
            prev_order.nxt = None
            self.tail = prev_order
        # hit corner case
        # else:
        #     pass

    def match_order(self, order, order_list):
        """
        Orders are added in FIFO style, starting from head.
        :param order:
        :param order_list:
        """
        # executed_orders = []
        executed_orders = Transactions()
        current_order = self.head
        # print("Cur Order ", current_order.peak_quantity)
        # print("Self Order ",self.head.peak_quantity)
        # Iterate and do trade
        while order.peak_quantity > 0 and self.length > 0:
            matched_order = current_order.match(order)
            if matched_order:
                current_next = current_order.nxt
                #         Current order is executed add to executed List and delete from list
                if current_order.peak_quantity == 0:
                    # executed_orders.append(current_order)
                    executed_orders.append(current_order, current_order.json_string())
                    del order_list[current_order.id]
                    self.delete_order(current_order)

                current_order = current_next
                # Start Over
                if current_next is None:
                    current_order = self.head

        for ordr in iter(self):
            if ordr.transaction_quantity > 0:
                # executed_orders.append(ordr)
                executed_orders.append(ordr, ordr.json_string())
        return executed_orders

    # Custom Iterator functionality
    def __iter__(self):
        self.iter_temp = self.head
        return self

    def __next__(self):
        if self.iter_temp is None:
            raise StopIteration
        else:
            val = self.iter_temp
            self.iter_temp = self.iter_temp.nxt
            self.visited = True
            return val
