from packet import PacketDecoder

import asyncio
import socket
import struct


class LineHandler:
    def __init__(self, config, packet_callback):
        self.config = config
        self.multicast_group = config['multicast_group']
        self.port = config['port']
        self.loop = asyncio.get_event_loop()
        self.transport = None
        self.packet_decoder = PacketDecoder()
        self.packet_callback = packet_callback

    async def connect(self):
        """
        Set up the multicast socket for receiving data.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("", self.port))

            mreq = struct.pack(
                '4s4s',
                socket.inet_aton(self.multicast_group),
                socket.inet_aton("0.0.0.0")
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            self.transport, _ = await self.loop.create_datagram_endpoint(
                lambda: MulticastProtocol(self), sock=sock
            )

            print(f"Connected to multicast group {self.multicast_group} on port {self.port}")
        except Exception as e:
            print(f"Failed to set up socket: {e}")

    async def disconnect(self):
        """
        Disconnect and clean up the socket.
        """
        if self.transport:
            self.transport.close()
            self.transport = None
            print("Socket disconnected.")

    def is_connected(self):
        return self.transport is not None


class MulticastProtocol(asyncio.DatagramProtocol):
    def __init__(self, handler):
        self.handler = handler

    def datagram_received(self, data, addr):
        """
        Handle incoming data.
        """
        packets = self.handler.packet_decoder.decode(data)
        self.handler.packet_callback(packets)

    def error_received(self, exc):
        """
        Handle socket errors.
        """
        print(f"Error received: {exc}")
