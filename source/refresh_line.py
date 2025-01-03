from line_handler import LineHandler
from packet import Packet
from typing import List


class RefreshService:
    def __init__(self, config):
        self.primary_line = LineHandler(config['channel1'],
                                        packet_callback=self.process_packet)
        self.secondary_line = LineHandler(config['channel2'],
                                          packet_callback=self.process_packet)

    def process_packet(self, packets: List[Packet]):
        pass

    def connect(self):
        return self.primary_line.connect() and self.secondary_line.connect()

    def disconnect(self):
        self.primary_line.disconnect()
        self.secondary_line.disconnect()
