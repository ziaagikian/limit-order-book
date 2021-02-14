from lib.src.orderStatus import OrderStatus
from datetime import datetime

db_date_format = "%Y-%m-%d %H:%M:%S.%f"


class Order(object):
    def __init__(self, id_, type_, price_, quantity_):
        self.id = id_
        self.type = type_
        self.price = price_
        self.peak_quantity = quantity_
        self.quantity = quantity_

        self.left_peak_quantity = quantity_ - self.peak_quantity
        self.order_status = OrderStatus(3)  # Mark as New
        self.eventTime = datetime.now().strftime(db_date_format)  # [:-4]
        #      Doubly Linked List
        self.nxt = None
        self.prev = None

        self.transaction_quantity = 0  # Track transaction quantity

    @property
    def is_buy(self):
        return self.type == "B" or self.type == "b"

    @property
    def is_sell(self):
        return self.type == "S" or self.type == "s"

    def match(self, incoming_order):
        """
        Atomic operation and can handle multiple requests at a time.
        :param incoming_order:
        :return: boolean
        """
        if incoming_order.type == self.type:
            return False
        if incoming_order.is_buy and incoming_order.price < self.price:
            return False
        # handle full size trade
        if self.peak_quantity <= incoming_order.peak_quantity:
            temp_quantity = self.peak_quantity
            # Update EventTime for saving in database
            self.eventTime = datetime.now().strftime(db_date_format)
            self.order_status = OrderStatus(1)  # Mark as Completed
            # update both orders
            self.do_trade(temp_quantity)
            incoming_order.do_trade(temp_quantity)
            return True
        # handle partial trade
        else:
            temp_quantity = incoming_order.peak_quantity
            # update both orders
            # Update EventTime for saving in database
            self.eventTime = datetime.now().strftime(db_date_format)
            self.order_status = OrderStatus(2)  # Mark as Partially Completed
            self.do_trade(temp_quantity)
            incoming_order.do_trade(temp_quantity)
            return False

    def do_trade(self, quantity):
        """
        Execute transaction Update remaining orders in Order book accordingly
        :param quantity:
        :return:
        """
        self.transaction_quantity += quantity
        self.peak_quantity -= quantity
        if self.peak_quantity == 0 and self.left_peak_quantity > 0:
            if self.left_peak_quantity >= self.quantity:
                self.peak_quantity += self.quantity
            else:
                self.peak_quantity += self.left_peak_quantity
            self.left_peak_quantity -= self.peak_quantity

    def restore_peak_quantity(self):
        """"""
        if self.left_peak_quantity > 0 and self.peak_quantity < self.quantity:
            diff = min(self.quantity - self.peak_quantity, self.left_peak_quantity)
            self.peak_quantity += diff
            self.left_peak_quantity -= diff

    def print_order(self):
        ordr_type = "Sell" if self.is_sell else "Buy"
        print("{:>9}|{:>12}|{:>12}|{:>10}|{:>20}".format(
            self.id, ordr_type, self.peak_quantity, self.price, self.order_status), end="")

    #  For Debugging
    def __str__(self):
        return "Order: type: {} id: {} price: {} qty {} event {}".format(self.type, self.id,
                                                                         self.price, self.quantity, self.eventTime)

    # For Saving in Database
    def json_string(self, unique_id=False):
        """
        JSON string to Save in database.
        :param unique_id: if True Make ID field as Unique to avoid duplication.
        :return: String in JSON format
        """
        ordr_type = "Sell" if self.is_sell else "Buy"
        if unique_id:
            json_data = {"_id": self.id, "price": self.price, "type": ordr_type, "quantity": self.quantity,
                         "status": str(self.order_status), "event_time": self.eventTime}
        else:
            json_data = {"id": self.id, "price": self.price, "type": ordr_type, "quantity": self.quantity,
                         "status": str(self.order_status), "event_time": self.eventTime}
        return json_data
