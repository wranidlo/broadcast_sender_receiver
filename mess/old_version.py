from PyQt5 import QtCore
from PyQt5.QtWidgets import QSplitter, QVBoxLayout, QDialog, QPushButton, QApplication, QTextEdit, QLineEdit

from mess.threded_listener import *

class Window(QDialog):
    def __init__(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        super().__init__()
        self.flag = 0
        self.chatTextField = QLineEdit(self)
        self.chatTextField.resize(480, 100)
        self.chatTextField.move(10, 350)
        self.btnSend = QPushButton("Send", self)
        self.btnSend.resize(480, 30)
        self.btnSendFont = self.btnSend.font()
        self.btnSendFont.setPointSize(15)
        self.btnSend.setFont(self.btnSendFont)
        self.btnSend.move(10, 460)
        self.btnSend.setStyleSheet("background-color: #F7CE16")
        self.btnSend.clicked.connect(self.send)

        self.chatBody = QVBoxLayout(self)
        # self.chatBody.addWidget(self.chatTextField)
        # self.chatBody.addWidget(self.btnSend)
        # self.chatWidget.setLayout(self.chatBody)
        splitter = QSplitter(QtCore.Qt.Vertical)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        # self.chatLayout=QVBoxLayout()
        # self.scrollBar=QScrollBar(self.chat)
        # self.chat.setLayout(self.chatLayout)

        splitter.addWidget(self.chat)
        splitter.addWidget(self.chatTextField)
        splitter.setSizes([400, 100])

        splitter2 = QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(self.btnSend)
        splitter2.setSizes([200, 10])

        self.chatBody.addWidget(splitter2)

        self.setWindowTitle("Chat Application")
        self.resize(500, 500)

    def send(self):
        text = self.chatTextField.text()
        font = self.chat.font()
        font.setPointSize(13)
        self.chat.setFont(font)
        text_formatted = '{:>80}'.format(text)
        self.chat.append(text_formatted)
        self.sender.sendto(text.encode("utf-8"), ("255.255.255.255", 37021))
        self.chatTextField.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    thread_listening = ThreadedListener(window)
    thread_listening.start()

    window.exec()

    thread_listening.kill()
    thread_listening.join()
    sys.exit(app.exec_())
