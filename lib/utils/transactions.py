
class Transactions:
    """
    Class Transaction hold executed Orders. Currently it contains two Lists.
    Fist list contains executed order in raw format, while the second one contains order in JSON format to save in database.
    """
    def __init__(self):
        self.executions = []
        self.executionsJson = []

    def __len__(self):
        return len(self.executions)

    def append(self, order, json_order):
        self.executions.append(order)
        self.executionsJson.append(json_order)

    def extend(self, order, json_order):
        self.executions.extend(order)
        self.executionsJson.extend(json_order)
