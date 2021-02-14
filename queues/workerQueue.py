from queue import Queue


class WorkerQueue(Queue):
    def __init__(self, type_, max_size=1, ):
        Queue.__init__(self, max_size)
        self._type = type_

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, new_type):
        self._type = new_type
