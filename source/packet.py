from message import Message, MessageHeader
import struct

from typing import List


class PacketHeader:
    def __init__(self, raw_data):
        """
        Initialize the PacketHeader object from raw binary data.
        """

        if len(raw_data) < self.size():
            raise ValueError(f"Insufficient data: expected {self.size()} bytes, got {len(raw_data)} bytes")

        # Unpack the binary data into fields
        unpacked = struct.unpack('<H B c I Q', raw_data[:self.size()])
        self.pkt_size, self.msg_count, filler_byte, self.seq_num, self.send_time = unpacked
        self.filler = filler_byte.decode('utf-8')

    @staticmethod
    def size():
        """
        Returns the total size of the packet header in bytes.
        """
        return 2 + 1 + 1 + 4 + 8  # PktSize + MsgCount + Filler + SeqNum + SendTime


class Packet:
    def __init__(self, raw_data):
        self.header = PacketHeader(raw_data)
        self.size = self.header.pkt_size
        self.messages = []
        for i in range(self.header.msg_count):
            message = Message(raw_data[PacketHeader.size() + i * MessageHeader.size():])
            self.messages.append(message)


class PacketDecoder:
    def __init__(self):
        self.data_buffer = bytearray()

    def decode(self, socket_data) -> List[Packet]:
        """
        Decode the raw binary data received from the socket into packets.

        Args:
            socket_data (bytes): The raw binary data received from the socket.

        Returns:
            List[Packet]: A list of Packet objects decoded from the raw binary data.
        """
        self.data_buffer.extend(socket_data)
        packets = []

        while len(self.data_buffer) >= PacketHeader.size():
            packet_header = PacketHeader(self.data_buffer)

            if len(self.data_buffer) < packet_header.pkt_size:
                break

            packet_data = self.data_buffer[:packet_header.pkt_size]
            packet = Packet(packet_data)
            packets.append(packet)

            self.data_buffer = self.data_buffer[packet_header.pkt_size:]

        return packets
