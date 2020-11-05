from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QListWidgetItem

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

    def send(self):
        text = self.line_edit_messege.text()
        item = QListWidgetItem(text)
        self.list_chat.addItem(item)
        self.sender.sendto(text.encode("utf-8"), ("255.255.255.255", 37021))
        self.line_edit_messege.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    thread_listening = ThreadedListener(window)
    thread_listening.start()

    window.exec()

    thread_listening.kill()
    thread_listening.join()
    sys.exit(app.exec_())
