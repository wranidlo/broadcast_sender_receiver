from PyQt5.QtWidgets import QApplication, QDialog, QScrollBar
from mess.threded_loader import *
from mess.gui import Ui_Dialog
import json
import netifaces as ni
import socket


def get_broadcasts_interfaces():
    broadcasts_list = []
    for e in ni.interfaces():
        try:
            broadcasts_list.append(ni.ifaddresses(e).get(2)[0].get("broadcast"))
        except TypeError:
            None
    return broadcasts_list


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

        self.load_broad_ip()
        self.update_info()

        self.button_synchronize.clicked.connect(self.update_info)

    def load_chat(self):
        self.list_chat.clear()
        file_info = open('chat.txt', 'r')
        lines = file_info.readlines()
        iterator = 1
        for line in lines:
            if iterator % 2 == 1:
                user = json.loads(line).get("user_ip")
                broadcast = json.loads(line).get("broadcast")
            else:
                if str(broadcast) == self.ip_broadcast:
                    if user == self.my_ip:
                        item = QListWidgetItem("-- Me --\n" + line.replace('\\n', '\n'))
                        item.setForeground(QtCore.Qt.blue)
                        item.setTextAlignment(QtCore.Qt.AlignLeft)
                    else:
                        item = QListWidgetItem("-- " + user + " --\n" + line.replace('\\n', '\n'))
                        item.setForeground(QtCore.Qt.black)
                        item.setTextAlignment(QtCore.Qt.AlignLeft)
                    self.list_chat.addItem(item)
                    self.list_chat.scrollToBottom()
            iterator += 1

    def send(self):
        message = self.line_edit_messege.toPlainText()
        message_json = {"message": message, "broadcast": self.ip_broadcast, "type": "communicator"}
        try:
            self.sender.sendto(json.dumps(message_json).encode("utf-8"), (self.ip_broadcast, 37021))
            item = QListWidgetItem("-- Me --\n" + message)
            item.setForeground(QtCore.Qt.blue)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            self.list_chat.addItem(item)
            self.line_edit_messege.setText("")
        except socket.error:
            self.ip_broadcast = "127.255.255.255"
            self.my_ip = "127.0.0.1"
            self.load_broad_ip()

    def change_ip(self):
        if self.combo_box_ip.currentText() == "127.255.255.255":
            self.ip_broadcast = "127.255.255.255"
            self.my_ip = "127.0.0.1"
        else:
            for e in ni.interfaces():
                if ni.ifaddresses(e).get(2)[0].get("broadcast") == self.combo_box_ip.currentText():
                    self.ip_broadcast = self.combo_box_ip.currentText()
                    self.my_ip = ni.ifaddresses(e).get(2)[0].get("addr")
                    break
        self.load_chat()
        self.update_info()

    def load_broad_ip(self):
        interfaces = get_broadcasts_interfaces()
        interfaces = list(dict.fromkeys(interfaces))
        self.combo_box_ip.clear()
        if "127.255.255.255" in interfaces:
            interfaces.remove("127.255.255.255")
        self.combo_box_ip.addItem("127.255.255.255")
        for e in interfaces:
            if e is not None:
                self.combo_box_ip.addItem(e)
        self.combo_box_ip.setCurrentText(self.ip_broadcast)

    def update_info(self):
        self.load_broad_ip()
        self.label_info.setText(str("Your ip: " + self.my_ip + " | Current broadcast: " + self.ip_broadcast))
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
