from PyQt5.QtWidgets import QApplication, QDialog, QScrollBar

from mess.threded_listener import *
from mess.gui import Ui_Dialog


class Window(Ui_Dialog, QDialog):
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        super(Window, self).__init__()
        self.setupUi(self)
        self.flag = 0

        self.button_send.clicked.connect(self.send)

        scroll_bar = QScrollBar(self)
        scroll_bar.setStyleSheet("background : lightgreen;")
        self.list_chat.setVerticalScrollBar(scroll_bar)

    def send(self):
        message = self.line_edit_messege.text()
        item = QListWidgetItem(message + " : Me")
        item.setForeground(QtCore.Qt.blue)
        item.setTextAlignment(QtCore.Qt.AlignRight)
        self.list_chat.addItem(item)
        self.sender.sendto(message.encode("utf-8"), ("255.255.255.255", 37021))
        self.line_edit_messege.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    thread_listening = ThreadedListener(window)
    thread_listening.start()

    window.show()
    app.exec_()

    thread_listening.kill()
    thread_listening.join()
