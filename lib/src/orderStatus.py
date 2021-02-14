from enum import Enum


class OrderStatus(Enum):
    COMPLETED = 1
    PARTIALLY_COMPLETED = 2
    NEW_ORDER = 3

    def __str__(self):
        return "{}".format(self.name)
