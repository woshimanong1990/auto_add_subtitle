# coding:utf-8
import os

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QDialog
from PySide2.QtGui import QPixmap

from ui_files.UI_main import Ui_MainWindow
from utils.view_utils import error_capture
from views.common_view import LoadingView
from views.show_message_dialog import MyDialog
from views.extract_audio_dialog import ExtractAudioDialog
from views.add_subtitle_dialog import AddSubtitleDialog
from views.transform_audio_dialog import TransformAudioDialog
from utils.variables import FileType


class MainWindow(QMainWindow, LoadingView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dialog = None
        self.file_type = FileType.video
        self.file_path = None

    @error_capture()
    def aboutAction(self, *args, **kwargs):
        self.dialog = MyDialog("""一个爱折腾的pythoner\n\n微信公众号：python码码有趣的\n\nqq群：389954854""")
        self.dialog.exec_()

    @error_capture()
    def declareAction(self, *args, **kwargs):
        self.dialog = MyDialog("本软件仅供交流学习，请勿商用。\n\n软件是对百度AI的简单的封装，语音识别效果可能有出入。")
        self.dialog.exec_()

    @error_capture()
    def helpAction(self, *args, **kwargs):
        self.dialog = MyDialog("1:配置软件目录下的settings.json（自行申请public key）\n\n2: 选择音频，自动生成srt字幕文件。可能比较需要点时间\n\n"
                          "3：其他工具辅助完成添加字幕\n\n")
        self.dialog.exec_()

    def mock_data(self):
        with open(r"E:\tmp\download\dog.jpg", 'rb') as f:
            self.image_bytes = f.read()

    @error_capture(need_info=True)
    def startAction(self, *args, **kwargs):
        pass

    @error_capture()
    def extracAudionAction(self, *args, **kwargs):
        self.dialog = ExtractAudioDialog()
        self.dialog.exec_()

    @error_capture()
    def transAudicoAction(self, *args, **kwargs):
        self.dialog = TransformAudioDialog()
        self.dialog.exec_()

    @error_capture()
    def addSubtitleAction(self, *args, **kwargs):
        self.dialog = AddSubtitleDialog()
        self.dialog.exec_()

    def selectFileAction(self, *args, **kwargs):
        file_path, _ = QFileDialog.getOpenFileName(None, "选择文件", "", "音频(*.wav)")
        if not file_path:
            QMessageBox.critical(None, '错误', '没有选择文件')
            return
        self.file_path = file_path
        self.ui.lineEdit.setText(self.file_path)

    @error_capture()
    def fileTypeSelectAction(self, index):
        if index == -2:
            self.file_type = FileType.audio
        else:
            self.file_type = FileType.video






def main():
    pass


if __name__ == "__main__":
    main()
