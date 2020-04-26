# coding:utf-8
import sys
from PySide2.QtWidgets import QApplication
from views.main import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
