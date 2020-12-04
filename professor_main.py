import sys
import os.path
from PyQt5 import QtCore
import netifaces as ni
from professor.listener import Sender
from professor.listener_thread import ThreadedListener, listen
from professor.profesor_gui import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem
import json


def get_broadcasts_interfaces():
    broadcasts_list = []
    for e in ni.interfaces():
        try:
            broadcasts_list.append(ni.ifaddresses(e).get(2)[0].get("broadcast"))
        except TypeError:
            None
    return broadcasts_list


class Window(Ui_Form, QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.sender = Sender()
        self.sender.set_broadcast_ip("127.255.255.255")
        self.student_list = []

        self.button_send_message.clicked.connect(self.send_message_broad)
        self.button_attendance.clicked.connect(self.attendance_check)
        self.button_add_student.clicked.connect(self.add_student_presence)
        self.load_presences()
        self.load_broad_ip()
        self.label_current_data.setText(str("Current broadcast: " + self.sender.ip_broadcast))
        self.button_change_broad.clicked.connect(self.change_ip)
        self.button_save_students.clicked.connect(self.save_attendance_list)
        self.button_clear_students.clicked.connect(self.clear_list_attendance)
        self.button_delete_student.clicked.connect(self.delete_student_attendance)
        self.load_students_absent()
        self.list_widget_absent.itemClicked.connect(self.click_student_absent)

    def load_students_absent(self):
        self.list_widget_absent.clear()
        file = open("professor/students_list")
        students_json = json.load(file)
        for e in students_json["students"]:
            if not any(d["index"] == e["index"] for d in self.student_list):
                item = QListWidgetItem(json.dumps(e))
                item.setForeground(QtCore.Qt.black)
                item.setTextAlignment(QtCore.Qt.AlignRight)
                self.list_widget_absent.addItem(item)
        self.label_absent_students.setText("Absent students: " + str(self.list_widget_absent.count()))

    def click_student_absent(self):
        student_json = json.loads(self.list_widget_absent.currentItem().text())
        self.line_edit_name.setText(student_json["name"])
        self.line_edit_surname.setText(student_json["surname"])
        self.line_edit_index.setText(student_json["index"])

    def send_message_broad(self):
        message = str(self.line_edit_message.text())
        message_json = json.dumps({"message": message, "who": "professor", "type": "message"})
        self.sender.send_broadcast_message(message_json.encode("utf-8"))
        item = QListWidgetItem(message)
        item.setForeground(QtCore.Qt.blue)
        item.setTextAlignment(QtCore.Qt.AlignLeft)
        self.list_send_messages.addItem(item)

    def attendance_check(self):
        message = str("Attendance check")
        message_json = json.dumps({"message": message, "who": "professor", "type": "attendance"})
        self.sender.send_broadcast_message(message_json.encode("utf-8"))

    def add_student_presence(self):
        name = self.line_edit_name.text()
        surname = self.line_edit_surname.text()
        index = self.line_edit_index.text()
        if not any(d["index"] == index for d in self.student_list):
            attendance = {"name": name, "surname": surname, "index": index}
            item = QListWidgetItem(json.dumps(attendance))
            item.setForeground(QtCore.Qt.blue)
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            self.list_widget_students.addItem(item)
            self.student_list.append(attendance)
            self.label_current_students.setText("Current students: " + str(len(self.student_list)))
        self.load_students_absent()

    def load_presences(self):
        self.list_widget_students.clear()
        if os.path.isfile('professor/presence.txt'):
            file_info = open('professor/presence.txt', 'r')
            lines = file_info.readlines()
            for line in lines:
                self.student_list.append(json.loads(line))
                item = QListWidgetItem(line)
                item.setForeground(QtCore.Qt.blue)
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                self.list_widget_students.addItem(item)
        self.label_current_students.setText("Current students: " + str(len(self.student_list)))

    def load_broad_ip(self):
        interfaces = get_broadcasts_interfaces()
        interfaces = list(dict.fromkeys(interfaces))
        self.combo_broad.clear()
        if "127.255.255.255" in interfaces:
            interfaces.remove("127.255.255.255")
        self.combo_broad.addItem("127.255.255.255")
        for e in interfaces:
            if e is not None:
                self.combo_broad.addItem(e)
        self.combo_broad.setCurrentText(self.sender.ip_broadcast)

    def change_ip(self):
        self.sender.set_broadcast_ip(self.combo_broad.currentText())
        self.label_current_data.setText(str("Current broadcast: " + self.sender.ip_broadcast))

    def save_attendance_list(self):
        open("professor/presence.txt", "w").close()
        for e in self.student_list:
            with open("professor/presence.txt", "a") as f:
                f.write(json.dumps(e) + "\n")

    def clear_list_attendance(self):
        self.student_list.clear()
        self.list_widget_students.clear()
        self.load_students_absent()
        self.label_current_students.setText("Current students: 0")

    def delete_student_attendance(self):
        try:
            selected_text = self.list_widget_students.currentItem().text()
            selected_row = self.list_widget_students.currentRow()
            self.list_widget_students.takeItem(selected_row)
            self.student_list.remove(json.loads(selected_text))
            self.load_students_absent()
        except Exception:
            None
        self.label_current_students.setText("Current students: " + str(len(self.student_list)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    s = ThreadedListener(target=listen, args=(window, ))
    s.start()

    window.show()
    app.exec_()

    s.kill()
    s.join()

    if not s.is_alive():
        print("Stopped listening for presence")
