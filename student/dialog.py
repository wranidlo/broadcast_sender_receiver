import sys
from PyQt5.QtWidgets import QWidget, QApplication
from student_main.attendance import *


class input_dialog(Ui_Form, QWidget):
    def __init__(self):
        super(input_dialog, self).__init__()
        self.setupUi(self)

    def send_presence(self):
        self.edit_full_name.text()


def main():
    app = QApplication(sys.argv)
    ex = input_dialog()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
