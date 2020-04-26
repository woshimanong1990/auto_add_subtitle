# coding:utf-8
import os

from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox
from views.common_view import LoadingView
from ui_files.UI_file_select import Ui_Dialog
from utils.view_utils import error_capture
from presents.extract_audio_present import ExtractAudioPresent


class ExtractAudioDialog(QDialog, LoadingView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("提取音频")
        self.out_dir = None
        self.select_file = None
        self.present = ExtractAudioPresent(self)
        self.file_format = "视频(*.mp4 *.mov *.flv)"

    @error_capture(need_info=True)
    def selectDirAction(self):
        select_dir = QFileDialog.getExistingDirectory(None, "请选择输出文件夹", "")
        if not select_dir:
            QMessageBox.critical(None, "错误", "请选择文件夹")
            return
        self.ui.dirLineEdit.setText(select_dir)
        self.out_dir = select_dir

    @error_capture(need_info=True)
    def selectFileAction(self):
        select_file, _ = QFileDialog.getOpenFileName(None, "请选择文件", "", self.file_format)
        if not select_file:
            QMessageBox.critical(None, "错误", "请选择文件")
            return
        self.ui.fileLineEdit.setText(select_file)
        self.select_file = select_file

    def check_params(self):
        if not self.out_dir:
            QMessageBox.critical(None, "错误", "请选择输出文件夹")
            return False
        if not self.select_file:
            QMessageBox.critical(None, "错误", "请选择视频文件")
            return False
        return True

    @error_capture(need_info=True)
    def startAction(self, *args, **kwargs):
        if not self.check_params():
            return
        self.show_loading()
        self.present.start(self.select_file, self.out_dir)

    @error_capture(need_info=True)
    def show_result(self, result, is_error):
        self.finish_loading()
        if is_error:
            QMessageBox.critical(None, '错误', str(result))
            return
        QMessageBox.information(None, "提示", "操作成功")
        if os.path.isdir(self.out_dir):
            os.startfile(self.out_dir)


def main():
    pass


if __name__ == "__main__":
    main()
