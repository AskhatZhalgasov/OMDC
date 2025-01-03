from source.line_arbitrage import LineArbitrage


class MessageHandler:
    def __init__(self, config):
        self.config = config
        self.real_time_line_arbitrage = LineArbitrage(config['real_time'])
        self.refresh_line_arbitrage = LineArbitrage(config['refresh'])

    def connect(self):
        return self.line_arbitrage.connect() and self.refresh_line_arbitrage.connect()

    def disconnect(self):
        self.line_arbitrage.disconnect()
        self.refresh_line_arbitrage.disconnect()

