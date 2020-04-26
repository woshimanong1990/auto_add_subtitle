# coding:utf-8
from views.extract_audio_dialog import ExtractAudioDialog


class TransformAudioDialog(ExtractAudioDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("转换音频")

    def startAction(self):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
