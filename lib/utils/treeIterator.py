class TreeIterator:
    """
    Return iterator for (Tree and Doubly Linkedlist).
    Fetch value of TreeNode-DoublyLinked ListNode before going to next node.
    """
    def __init__(self, itr):
        self.tree_iter = iter(itr)
        self.order_iter = None
        self.next_tree_node = None
        # Order val
        self.next_order_val = None
        self.has_next = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_next:
            res = self.next_order_val
        else:
            res = next(self.order_iter)
        self.has_next = None
        return res

    def hasnext(self):
        if self.has_next is None:
            try:
                # First time called -> tree_node is None go to next
                if self.next_tree_node is None:
                    self.next_tree_node = next(self.tree_iter)
                    self.order_iter = iter(self.next_tree_node)
                self.next_order_val = next(self.order_iter)
            except StopIteration:
                try:
                    #  move to next TreeNode
                    self.next_tree_node = next(self.tree_iter)
                    self.order_iter = iter(self.next_tree_node)
                    self.next_order_val = next(self.order_iter)
                except StopIteration:
                    self.has_next = False
                else:
                    self.has_next = True
            else:
                self.has_next = True
        return self.has_next
