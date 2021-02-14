from enum import Enum


class QueueType(Enum):
    HISTORY_QUEUE = 1
    TRANSACTIONS_QUEUE = 2

    def __str__(self):
        return "{}".format(self.name)
