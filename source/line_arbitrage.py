from packet import Packet

from line_handler import LineHandler

from typing import List

from collections import queue


class LineArbitrage:
    def __init__(self, config):
        self.config = config
        self.primary_line = LineHandler(config['channel1'],
                                        packet_callback=self.process_packet)
        self.secondary_line = LineHandler(config['channel2'],
                                          packet_callback=self.process_packet)

        self.expected_sequence_number = None
        self.is_gap_detected = False
        self.buffered_messages = queue.Queue()

    def connect(self):
        return self.primary_line.connect() and self.secondary_line.connect()

    def process_message(self, message):
        pass

    def process_buffered_packets(self):
        """
        Process any buffered packets that can now be processed.
        """

        while len(self.buffered_messages) > 0:
            message = self.buffered_messages[0]
            if message.header.seq_num < self.expected_sequence_number:
                # Ignore messages that have already been processed
                self.buffered_messages.pop(0)
                continue
            if message.header.seq_num == self.expected_sequence_number:
                self.process_message(message)
                self.buffered_packets.pop(0)
                self.expected_sequence_number += 1
            else:
                break

        self.is_gap_detected = (len(self.buffered_messages) == 0)

    def process_packet(self, packetList: List[Packet]):
        """
        Process a packet of data.
        """

        for packet in packetList:
            if self.expected_sequence_number is None:
                self.expected_sequence_number = packet.header.seq_num

            if packet.header.seq_num + packet.header.msg_count < self.expected_sequence_number:
                # Ignore packets that have already been processed
                continue

            for index, message in enumerate(packet.messages):
                current_sequence_number = packet.header.seq_num + index
                if current_sequence_number < self.expected_sequence_number:
                    # Ignore messages that have already been processed
                    continue

                if current_sequence_number == self.expected_sequence_number:
                    # Process the message
                    self.process_message(message)
                    self.expected_sequence_number += 1

                    # Check if there are any buffered packets that can be processed
                    self.process_buffered_packets()

                if current_sequence_number > self.expected_sequence_number:
                    # Buffer the packet
                    self.buffered_packets.append(packet)
                    self.is_gap_detected = True
