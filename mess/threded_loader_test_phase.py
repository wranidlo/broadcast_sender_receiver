import socket
import threading
import sys
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
import json
import time


class ThreadedLoader(threading.Thread):
    def __init__(self, window, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        self.window = window
        self.lines_number = 0

    def run(self):
        while True:
            file1 = open('mess/chat.txt', 'r')
            lines = file1.readlines()
            if len(lines) > self.lines_number:
                self.lines_number = len(lines)
                self.window.list_chat.clear()
                for line in lines:
                    user_ip = json.loads(line).get("user_ip")
                    user_port = json.loads(line).get("user_port")
                    message = json.loads(line).get("message")

                    # delete checking user port when not on localhost
                    try:
                        if str(user_ip) == str(self.window.my_ip):#  and int(user_port) == int(self.window.my_ip[1]):
                            item = QListWidgetItem(message + " : " + "Me")
                            item.setForeground(QtCore.Qt.blue)
                            item.setTextAlignment(QtCore.Qt.AlignRight)
                        else:
                            item = QListWidgetItem(user_ip + " : " + message)
                            item.setForeground(QtCore.Qt.black)
                            item.setTextAlignment(QtCore.Qt.AlignLeft)
                        self.window.list_chat.addItem(item)
                    except TypeError:
                        print("No address ip yet")
            self.window.list_chat.scrollToBottom()
            time.sleep(0.25)

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
    s = ThreadedLoader()
    s.start()
    s.kill()
    s.join()
