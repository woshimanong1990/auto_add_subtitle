# coding:utf-8
import os

from PySide2.QtWidgets import QDialog, QFileDialog, QMessageBox

from views.common_view import LoadingView
from ui_files.UI_add_subtitle import Ui_Dialog
from presents.add_subtitle_present import AddSubtitlePresent
from utils.view_utils import error_capture
from views.common_view import LoadingView


class AddSubtitleDialog(QDialog, LoadingView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("添加字幕")
        self.present = AddSubtitlePresent(self)
        self.video_file = None
        self.srt_file = None

    @error_capture(need_info=True)
    def selectSubtitleAction(self):
        select_file, _ = QFileDialog.getOpenFileName(None, "请选择文件", "", "字幕(*.srt)")
        if not select_file:
            QMessageBox.critical(None, "错误", "请选择文件")
            return
        self.srt_file = select_file
        self.ui.subtitleLineEdit.setText(select_file)

    @error_capture(need_info=True)
    def selectVideoAction(self):
        select_file, _ = QFileDialog.getOpenFileName(None, "请选择文件", "", "视频(*.mp4 *.mov *.flv)")
        if not select_file:
            QMessageBox.critical(None, "错误", "请选择文件")
            return
        self.video_file = select_file
        self.ui.videoEdit.setText(select_file)

    def check_param(self):
        if not self.srt_file:
            QMessageBox.critical(None, "错误", "请选择字幕文件")
            return False
        if not self.video_file:
            QMessageBox.critical(None, "错误", "请选择视频文件")
            return False
        return True

    @error_capture(need_info=True)
    def startAction(self):
        if not self.check_param():
            return
        self.show_loading()
        self.present.start(self.video_file, self.srt_file)

    @error_capture(need_info=True)
    def show_result(self, result, is_error):
        self.finish_loading()
        if is_error:
            QMessageBox.critical(None, '错误', str(result))
            return
        QMessageBox.information(None, "提示", "操作成功")
        dir_name = os.path.dirname(self.video_file)
        if self.video_file and os.path.isdir(dir_name):
            os.startfile(dir_name)


def main():
    pass


if __name__ == "__main__":
    main()
