from PyQt5.QtWidgets import QApplication, QDialog, QScrollBar

from mess.threded_loader import *
from mess.gui import Ui_Dialog
import json
import netifaces as ni
import socket


class Window(Ui_Dialog, QDialog):
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ip_broadcast = "127.255.255.255"
        self.my_ip = "127.0.0.1"
        super(Window, self).__init__()
        self.setupUi(self)
        self.flag = 0

        self.button_send.clicked.connect(self.send)
        self.button_ip.clicked.connect(self.change_ip)

        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : lightgreen;")
        self.list_chat.setVerticalScrollBar(scroll_bar)

    def load_chat(self):
        file = open('mess/chat.txt', 'r')
        lines = file.readlines()
        for line in lines:
            try:
                user = json.loads(line).get("user_ip")
                message = json.loads(line).get("message")
                if str(json.loads(line).get("broadcast")) == self.ip_broadcast:
                    if user == self.my_ip:
                        item = QListWidgetItem(message + " : Me")
                        item.setForeground(QtCore.Qt.blue)
                        item.setTextAlignment(QtCore.Qt.AlignRight)
                    else:
                        item = QListWidgetItem(user + " : " + message)
                        item.setForeground(QtCore.Qt.black)
                        item.setTextAlignment(QtCore.Qt.AlignLeft)
                    self.list_chat.addItem(item)
            except json.decoder.JSONDecodeError:
                print("Encoder error")

    def send(self):
        message = self.line_edit_messege.text()
        message_json = {"message": message, "broadcast": self.ip_broadcast, "type": "communicator"}
        try:
            self.sender.sendto(json.dumps(message_json).encode("utf-8"), (self.ip_broadcast, 37021))
            item = QListWidgetItem(message + " : Me")
            item.setForeground(QtCore.Qt.blue)
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.list_chat.addItem(item)
            self.line_edit_messege.setText("")
        except socket.error:
            self.ip_broadcast = "127.255.255.255"
            self.my_ip = "127.0.0.1"
            self.line_edit_ip.setText("Wrong address")

    def change_ip(self):
        self.list_chat.clear()
        if self.line_edit_ip.text() == "127.255.255.255":
            self.ip_broadcast = "127.255.255.255"
            self.my_ip = "127.0.0.1"
        else:
            for e in ni.interfaces():
                try:
                    if ni.ifaddresses(e).get(2)[0].get("broadcast") == self.line_edit_ip.text():
                        self.ip_broadcast = self.line_edit_ip.text()
                        self.my_ip = ni.ifaddresses(e).get(2)[0].get("addr")
                        break
                except:
                    self.line_edit_ip.setText("Wrong address")
        self.load_chat()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    window.load_chat()
    thread_listening = ThreadedLoader(window)
    thread_listening.start()

    window.show()
    app.exec_()

    thread_listening.kill()
    thread_listening.join()
