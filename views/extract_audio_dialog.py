# coding:utf-8

from PySide2.QtWidgets import QDialog
from views.common_view import LoadingView
from ui_files.UI_file_select import Ui_Dialog


class ExtractAudioDialog(QDialog, LoadingView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("提取音频")

    def selectDirAction(self):
        pass

    def selectFileAction(self):
        pass

    def startAction(self):
        pass



def main():
    pass


if __name__ == "__main__":
    main()
