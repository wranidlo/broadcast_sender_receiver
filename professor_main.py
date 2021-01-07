import json
import os.path
import smtplib
import ssl
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import netifaces as ni
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QListWidgetItem, QTreeWidgetItem

from professor.listener import Sender
from professor.listener_thread import ThreadedListener, listen
from professor.profesor_gui import Ui_Form


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

        self.combo_box_email.addItem("All students")
        self.combo_box_email.addItem("Absent students")
        self.button_email.clicked.connect(self.send_email)

        self.button_activity.clicked.connect(self.activity_check)
        self.list_activities = {}
        self.combo_box_student_activity.currentTextChanged.connect(self.load_activity_of_student)

    def send_email(self):
        port = 587  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = self.line_edit_email.text()
        password = self.line_edit_password.text()
        content = self.text_edit_emails.toPlainText()
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        counter_of_emails = 0
        message = MIMEMultipart("alternative")
        message["Subject"] = self.line_edit_subject.text()
        message["From"] = sender_email
        content_mime = MIMEText(content, "plain")

        try:
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls(context=context)
                server.login(sender_email, password)
                if self.combo_box_email.currentText() == "All students":
                    file = open("home/vagrant/.virtualabinfo", "r")
                    students_json = json.load(file)
                    for e in students_json["professor"]["students"]:
                        e["index"] = e["albumnr"]
                        del e["albumnr"]
                        del e["ip"]
                        del e["professorip"]
                        if e["email"] != "empty":
                            message["To"] = e["email"]
                            message.attach(content_mime)
                            self.list_widget_emails.clear()
                            item = QListWidgetItem(e["email"])
                            self.list_widget_emails.addItem(item)
                            server.sendmail(sender_email, e["email"], message.as_string())
                            counter_of_emails += 1
                if self.combo_box_email.currentText() == "Absent students":
                    for i in range(self.list_widget_absent.count()):
                        student_json = json.loads(self.list_widget_absent.item(i).text())
                        if student_json["email"] != "empty":
                            message["To"] = student_json["email"]
                            message.attach(content_mime)
                            self.list_widget_emails.clear()
                            item = QListWidgetItem(student_json["email"])
                            self.list_widget_emails.addItem(item)
                            server.sendmail(sender_email, student_json["email"], message.as_string())
                            counter_of_emails += 1
                self.label_email_status.setText("Email authentication ok\n"
                                                "Send to " + str(counter_of_emails) + " students")
        except smtplib.SMTPAuthenticationError:
            self.label_email_status.setText("Email authentication error\nCheck your email and password")

    def load_students_absent(self):
        self.list_widget_absent.clear()
        file = open("home/vagrant/.virtualabinfo", "r")
        students_json = json.load(file)
        for e in students_json["professor"]["students"]:
            e["index"] = e["albumnr"]
            del e["albumnr"]
            del e["ip"]
            del e["professorip"]
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

    def activity_check(self):
        try:
            message = str("Activity check")
            self.list_activities.clear()
            message_json = json.dumps({"message": message, "who": "professor", "type": "activity"})
            self.sender.send_broadcast_message(message_json.encode("utf-8"))
            self.label_activity_status.setText("Activity check - done")
        except:
            self.label_activity_status.setText("Something went wrong, check your ethernet connection")

    def load_activity_of_student(self):
        self.tree_widget_activity.clear()
        app_list = self.list_activities[self.combo_box_student_activity.currentText()]
        app_info = [[e["app"], e["time"], e["percentage"], e["windows"]] for e in app_list]
        self.tree_widget_activity.setHeaderItem(QTreeWidgetItem(["Name", "Time", "Percentage"]))
        for e in app_info:
            app_root = QTreeWidgetItem(self.tree_widget_activity, e[:3])
            w_lists = [x for x in e[3]]
            w_info = [[e["window_name"], e["window_time"], e["window_percentage"]] for e in w_lists]
            for f in w_info:
                window_root = QTreeWidgetItem(app_root, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()

    s = ThreadedListener(target=listen, args=(window,))
    s.start()

    window.show()
    app.exec_()

    s.kill()
    s.join()

    if not s.is_alive():
        print("Stopped listening for presence")
