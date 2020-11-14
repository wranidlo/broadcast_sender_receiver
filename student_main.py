import socket
import os
import logging
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from student.attendance import *


def send_presence():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = input("Your name and surname: ")
    ip_broadcast = str(os.system("ifconfig | grep broadcast | awk '{print $NF}'"))
    s.sendto(str(message).encode("utf-8"), (ip_broadcast, 37021))
    print("message sent!")


class input_dialog(Ui_Attendance, QWidget):
    def __init__(self):
        super(input_dialog, self).__init__()
        self.setupUi(self)
        self.button_send.clicked.connect(self.send_presence)

    def send_presence(self):
        message = self.edit_full_name.text()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # ip_broadcast = str(os.system("ifconfig | grep broadcast | awk '{print $NF}'"))
        ip_broadcast = "255.255.255.255"
        s.sendto(str(message).encode("utf-8"), (ip_broadcast, 37021))
        self.close()

class Client:
    def __init__(self):
        self.logger = logging.getLogger('broadcast_app')
        handler = logging.FileHandler('broadcast_app.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.client.bind(("", 37020))
        print(self.client.getsockname())
        print("Listening")

    def receive_message(self, length):
        return self.client.recvfrom(length)


if __name__ == '__main__':
    student = Client()
    student.start()
    while True:
        data, addr = student.receive_message(1024)
        data = data.decode("utf-8")
        os.system("notify-send \"Message\" \"%s\"" % data)
        if data == "Attendance check":
            app = QApplication(sys.argv)
            ex = input_dialog()
            ex.show()
            app.exec_()
        student.logger.info(data)
