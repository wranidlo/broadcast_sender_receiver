import socket
from datetime import date
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
import threading
import sys
import json


def listen(window):
    listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.settimeout(1)
    listener.bind(("", 37020))
    while True:
        try:
            message, addr = listener.recvfrom(4096)
            message = message.decode("utf-8")
            print("Presence reported: ", message)
            item = QListWidgetItem(message)
            item.setForeground(QtCore.Qt.blue)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            window.list_widget_students.addItem(item)
            f = open("presence.txt ", "a")
            f.write(message + "\n")
            f.close()
        except socket.timeout:
            None


class ThreadedListener(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


if __name__ == '__main__':
    s = ThreadedListener()
    s.start()
    s.kill()
    s.join()
