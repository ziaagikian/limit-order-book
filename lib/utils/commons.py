import sys


def print_benchmark(total_orders, total_time) -> None:
    """
    Print Benchmarked results or Performance Matrix
    :param total_orders: Total Orders
    :param total_time: Total Time
    :return: None
    """
    sys.stdout.write('{0} orders processed over {1:.2f} seconds.\n'.format(total_orders, total_time))
    sys.stdout.write("Average speed is {0:.0f} orders/second or {1:.2f} microseconds/order,\n".format((total_orders / total_time), (
                total_time / total_orders) * 1000 * 1000))
