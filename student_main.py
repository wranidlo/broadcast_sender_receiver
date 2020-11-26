import socket
import os
import sys
import json

from PyQt5.QtWidgets import QWidget, QApplication
from student.attendance import *


class input_dialog(Ui_Attendance, QWidget):
    def __init__(self, address):
        super(input_dialog, self).__init__()
        self.setupUi(self)
        self.addr = address
        self.button_send.clicked.connect(self.send_presence)

    def send_presence(self):
        name = self.line_edit_name.text()
        surname = self.line_edit_surname.text()
        index = self.line_edit_index.text()
        message = {"name": name, "surname": surname, "index": index}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendto(str(json.dumps(message)).encode("utf-8"), (str(self.addr), 37020))
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


def pop_up_dialog(address):
    app = QApplication(sys.argv)
    ex = input_dialog(address[0])
    ex.show()
    app.exec_()


if __name__ == '__main__':
    student = Client()
    student.start()
    while True:
        data, addr = student.receive_message(1024)
        data = json.loads(data.decode("utf-8"))
        if data.get("type") == "communicator":
            os.system("notify-send \"Message from communicator\" \"%s\"" % data.get("message"))
            with open("mess/chat.txt", "a") as outfile:
                outfile.write('{"user_ip": "' + str(addr[0]) + '", "broadcast": "' + str(data.get("broadcast")) +
                              '"}\n')
                outfile.write(str(data.get("message").replace('\n', '\\n'))+"\n")
        else:
            if data.get("type") == "attendance":
                os.system("notify-send \"Attendance check\" \"%s\"" % data.get("message"))
                pop_up_dialog(addr)
            else:
                os.system("notify-send \"Message from professor\" \"%s\"" % data.get("message"))
