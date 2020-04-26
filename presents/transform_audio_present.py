# coding:utf-8

import os
from presents.common_present import CommonPresent


class ExtractAudioPresent(CommonPresent):

    def process_audio(self, audio_file, audio_dir):
        trans_audio_file = audio_file
        if not self.check_audio_should_trans(audio_file):
            trans_audio_file = os.path.join(audio_dir, "{}.wav".format(os.path.splitext(os.path.basename(audio_file))[0]))
            self.transform_audio(audio_file, trans_audio_file)
        return trans_audio_file

    def start(self, audio_file, audio_dir):
        self.model.start(self.view.show_result, self.process_audio, audio_file, audio_dir)


def main():
    pass


if __name__ == "__main__":
    main()
