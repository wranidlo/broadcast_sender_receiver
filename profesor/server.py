import socket
from os import system

class Sender:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ip_broadcast = ""

    def set_broadcast_ip(self):
        # self.ip_broadcast = str(system("ifconfig | grep broadcast | awk '{print $NF}'"))
        self.ip_broadcast = "255.255.255.255"

    def send_broadcast_message(self, message):
        self.server.sendto(message, (self.ip_broadcast, 37020))
        print("message sent!")
