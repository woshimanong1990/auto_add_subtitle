# coding:utf-8
import os
from presents.common_present import CommonPresent


class ExtractAudioPresent(CommonPresent):
    def start(self, video, audio_dir):
        audio_file = os.path.join(audio_dir, "{}.wav".format(os.path.splitext(os.path.basename(video))[0]))
        self.model.start(self.view.show_result, self.extract_audio, video, audio_file_path=audio_file)


def main():
    pass


if __name__ == "__main__":
    main()
