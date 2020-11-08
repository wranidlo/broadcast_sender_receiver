import socket
import threading
import sys
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore


class ThreadedListener(threading.Thread):
    def __init__(self, window, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.window = window
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.listener.settimeout(1)
        self.listener.bind(("", 37021))

    def run(self):
        while True:
            try:
                data, addr = self.listener.recvfrom(2048)
                if data.decode("utf-8") == "This message is for starting 1.982789":
                    continue
                if addr[1] != self.window.sender.getsockname()[1]:
                    item = QListWidgetItem(addr[0] + " : " + data.decode("utf-8"))
                    item.setForeground(QtCore.Qt.black)
                    item.setTextAlignment(QtCore.Qt.AlignLeft)
                    self.window.list_chat.addItem(item)
            except socket.timeout:
                None

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
