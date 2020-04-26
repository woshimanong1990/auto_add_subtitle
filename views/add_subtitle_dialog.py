# coding:utf-8

from PySide2.QtWidgets import QDialog
from views.common_view import LoadingView
from ui_files.UI_add_subtitle import Ui_Dialog


class AddSubtitleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("添加字幕")


    def selectSubtitleAction(self):
        pass

    def selectVideoAction(self):
        pass

    def startAction(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
