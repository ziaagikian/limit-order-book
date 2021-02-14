import time

from lib.src.order import Order
from lib.src.orderBook import OrderBook
from lib.utils.commons import *


def main():
    order_book = OrderBook()
    tic = time.time()
    orders_executed = 0  # Order counter

    while True:
        try:
            line = sys.stdin.readline()
            fields = line.split(",")
            # EOF
            if not line:
                order_book.print_real_time_order_book()
                sys.stderr.write("End of File.\n")
                break
            ord_type = fields[0]  # B or S
            ord_id = fields[1]
            ord_price = int(fields[2])
            ord_qty = int(fields[3])

            order = Order(ord_id, ord_type, ord_price, ord_qty)
            order_book.execute_order(order)

        except KeyboardInterrupt:
            break
        orders_executed += 1

    toc = time.time()
    executed_time = toc - tic
    print_benchmark(orders_executed, executed_time)


if __name__ == "__main__":
    main()
