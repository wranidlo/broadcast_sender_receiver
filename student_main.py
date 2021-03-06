import socket
import os
import sys
import json

from PyQt5.QtWidgets import QWidget, QApplication
from student.attendance import *


class input_dialog(Ui_Attendance, QWidget):
    def __init__(self, address):
        super(input_dialog, self).__init__()
        self.setupUi(self)
        self.addr = address
        self.button_send.clicked.connect(self.send_presence)

        with open(os.path.expanduser("~/.virtualabinfo"), "r") as json_file:
            data = json_file.read()
            data = data.replace('u"', '"')
            with open("Output", "w") as text_file:
                text_file.write(data)
        with open("Output", "r") as file:
            user_json = json.load(file)
            if "student" in user_json:
                self.line_edit_name.setText(user_json["student"]["name"])
                self.line_edit_index.setText(user_json["student"]["albumnr"])
                self.line_edit_surname.setText(user_json["student"]["surname"])
                self.line_edit_email.setText(user_json["student"]["email"])

    def send_presence(self):
        name = self.line_edit_name.text()
        surname = self.line_edit_surname.text()
        index = self.line_edit_index.text()
        email = self.line_edit_email.text()
        message = {"type": "attendance", "name": name, "surname": surname, "index": index, "email": email}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendto(str(json.dumps(message)).encode("utf-8"), (str(self.addr), 37020))
        self.close()


class Client:
    def __init__(self):
        # with open(os.path.expanduser("~/.virtualabinfo"), "r") as json_file:
        #     data = json_file.read()
        #     data = data.replace('u"', '"')
        #     with open("Output", "w") as text_file:
        #         text_file.write(data)
        # with open("Output", "r") as file:
        #     user_json = json.load(file)
        #     if "student" in user_json:
        #         self.user_name = user_json["student"]["name"]+user_json["student"]["surname"]
        #         self.type = "student"
        #     else:
        #         self.user_name = user_json["professor"]["name"] + user_json["professor"]["surname"]
        #         self.type = "professor"

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self.client.bind(("", 37021))

    def receive_message(self, length):
        return self.client.recvfrom(length)


def pop_up_dialog(address):
    app = QApplication(sys.argv)
    ex = input_dialog(address[0])
    ex.show()
    app.exec_()


def send_activity(address, sender):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    f = open("/etc/virtualab/vm-communicator/log_activity.json", "r")
    jf = json.load(f)
    s.sendto(json.dumps({"type": "activity", "sender": sender, "data": jf}).encode("utf-8"), (address[0], 37020))


if __name__ == '__main__':
    user = Client()
    user.start()
    os.system("export DISPLAY=:0.0")
    os.system("XDG_RUNTIME_DIR=/run/user/$(id -u)")

    while True:
        data, addr = user.receive_message(1024)
        data = json.loads(data.decode("utf-8"))
        if data.get("type") == "communicator":
            os.system("notify-send \"Message from " + str(data.get("sender")) + " \" \"%s\"" % data.get("message"))
            with open("/etc/virtualab/vm-communicator/mess/chat.txt", "a") as outfile:
                outfile.write('{"user_ip": "' + str(addr[0]) + '", "broadcast": "' + str(data.get("broadcast")) +
                              '", "sender": "' + str(data.get("sender")) + '"}\n')
                outfile.write(str(data.get("message").replace('\n', '\\n')) + "\n")
        else:
            #  Reading json here
            with open(os.path.expanduser("~/.virtualabinfo"), "r") as json_file:
                raw_file = json_file.read()
                raw_file = raw_file.replace('u"', '"')
                with open("Output", "w") as text_file:
                    text_file.write(raw_file)
            with open("Output", "r") as file:
                user_json = json.load(file)
                if "student" in user_json:
                    user_name = user_json["student"]["name"] + user_json["student"]["surname"]
                    user_type = "student"
                else:
                    user_name = user_json["professor"]["name"] + user_json["professor"]["surname"]
                    user_type = "professor"

            if data.get("type") == "attendance":
                if user_type == "student":
                    os.system("notify-send \"Attendance check\" \"%s\"" % data.get("message"))
                    pop_up_dialog(addr)
                else:
                    os.system("notify-send \"Attendance check\" \"%s\"" % "You started attendance check")
            else:
                if data.get("type") == "activity":
                    if user_type == "student":
                        os.system("notify-send \"Activity check\" \"%s\"" % data.get("message"))
                        send_activity(addr, user_name)
                    else:
                        os.system("notify-send \"Activity check\" \"%s\"" % "You started activity check")
                else:
                    os.system("notify-send \"Message from professor\" \"%s\"" % data.get("message"))
