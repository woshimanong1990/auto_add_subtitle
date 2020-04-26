# coding:utf-8
from views.extract_audio_dialog import ExtractAudioDialog, error_capture
from presents.transform_audio_present import TransformAudioPresent


class TransformAudioDialog(ExtractAudioDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("转换音频")
        self.present = TransformAudioPresent(self)
        self.file_format = "音频(*.wav *.mp3)"

    @error_capture(need_info=True)
    def startAction(self):
        if not self.check_params():
            return
        self.show_loading()
        self.present.start(self.select_file, self.out_dir)


def main():
    pass


if __name__ == "__main__":
    main()
