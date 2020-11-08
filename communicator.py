from PyQt5.QtWidgets import QApplication, QDialog, QScrollBar

from mess.threded_listener import *
from mess.gui import Ui_Dialog


class Window(Ui_Dialog, QDialog):
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.ip_broadcast = "255.255.255.255"
        super(Window, self).__init__()
        self.setupUi(self)
        self.flag = 0

        self.button_send.clicked.connect(self.send)
        self.button_ip.clicked.connect(self.change_ip)

        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : lightgreen;")
        self.list_chat.setVerticalScrollBar(scroll_bar)

    def send(self):
        message = self.line_edit_messege.text()
        try:
            self.sender.sendto(message.encode("utf-8"), (self.ip_broadcast, 37021))
            item = QListWidgetItem(message + " : Me")
            item.setForeground(QtCore.Qt.blue)
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.list_chat.addItem(item)
            self.line_edit_messege.setText("")
        except socket.error:
            self.ip_broadcast = "255.255.255.255"
            self.line_edit_ip.setText("Wrong  address")

    def change_ip(self):
        self.ip_broadcast = self.line_edit_ip.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    window.sender.sendto(str("This message is for starting 1.982789").encode("utf-8"), (window.ip_broadcast, 37021))

    thread_listening = ThreadedListener(window)
    thread_listening.start()

    window.show()
    app.exec_()

    thread_listening.kill()
    thread_listening.join()
