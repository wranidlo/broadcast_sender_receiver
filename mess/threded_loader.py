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
            file = open('mess/chat.txt', 'r')
            lines = file.readlines()
            if len(lines) > self.lines_number:
                self.lines_number = len(lines)
                self.window.list_chat.clear()
                iterator = 1
                for line in lines:
                    if iterator % 2 == 1:
                        line_json = json.loads(line)
                        user_ip = line_json.get("user_ip")
                        broadcast = line_json.get("broadcast")
                    else:
                        if str(broadcast) == self.window.ip_broadcast:
                            if str(user_ip) == str(self.window.my_ip):
                                item = QListWidgetItem("-- Me --\n" + line.replace('\\n', '\n'))
                                item.setForeground(QtCore.Qt.blue)
                                item.setTextAlignment(QtCore.Qt.AlignLeft)
                            else:
                                item = QListWidgetItem("-- " + user_ip + " --\n" + line.replace('\\n', '\n'))
                                item.setForeground(QtCore.Qt.green)
                                item.setTextAlignment(QtCore.Qt.AlignLeft)
                            self.window.list_chat.addItem(item)
                    iterator += 1
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
