import socket
import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication
from student.attendance import *


class input_dialog(Ui_Attendance, QWidget):
    def __init__(self, addr):
        super(input_dialog, self).__init__()
        self.setupUi(self)
        self.addr = addr
        self.button_send.clicked.connect(self.send_presence)

    def send_presence(self):
        message = self.edit_full_name.text()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendto(str(message).encode("utf-8"), (str(self.addr), 37020))
        self.close()


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.client.bind(("", 37021))
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
        print(data)
        if data != "Attendance check":
            os.system("notify-send \"Message\" \"%s\"" % data)
            with open("mess/chat.txt", "a") as outfile:
                outfile.write('{"user_ip": "' + addr[0] + '", "user_port": "' + str(addr[1]) + '", "message":"' + data + '"}\n')
        else:
            os.system("notify-send \"Message\" \"%s\"" % data)
            app = QApplication(sys.argv)
            ex = input_dialog(addr[0])
            ex.show()
            app.exec_()
