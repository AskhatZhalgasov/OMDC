
from collections import defaultdict

class OrderBook:
    def __init__(self):
        self.bids = defaultdict(list[int])
        self.asks = defaultdict(list[int])


    def process_update_message(self, message):
        pass

    def process_trade_message(self, message):
        pass

    def add_order(self, price, quantity, side):
        pass

    def remove_order(self, orderId):
        pass

    def get_best_bid(self):
        pass
