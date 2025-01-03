import struct


class MessageHeader:
    def __init__(self, raw_data):
        """
        Initialize the MessageHeader object from raw binary data.
        """
        if len(raw_data) < self.size():
            raise ValueError(f"Insufficient data: expected {self.size()} bytes, got {len(raw_data)} bytes")

        # Unpack the binary data into fields
        unpacked = struct.unpack('<H H', raw_data[:self.size()])
        self.msg_size, self.msg_type = unpacked

    @staticmethod
    def size():
        """
        Returns the total size of the message header in bytes.
        """
        return 2 + 2  # MsgSize (2 bytes) + MsgType (2 bytes)


class Message:
    def __init__(self, raw_data):
        """
        Initialize the Message object from raw binary data.
        """

        self.header = MessageHeader(raw_data)

        # TODO: Parse the message body based on the message type
        self.body = raw_data[MessageHeader.size():]
