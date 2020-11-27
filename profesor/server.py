import socket


class Sender:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ip_broadcast = "127.255.255.255"

    def set_broadcast_ip(self, ip):
        self.ip_broadcast = str(ip)

    def send_broadcast_message(self, message):
        self.server.sendto(message, (self.ip_broadcast, 37021))
        print("message sent!")
