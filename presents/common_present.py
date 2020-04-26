# coding:utf-8
import os
import wave
from models.model import Model

from utils.process_utils import extra_audio_and_transform, combine_video_and_srt
from auto_add_subtitle.utils.media_utils import cut_audio
from auto_add_subtitle.utils.request_utils import parse_audio_baidu
from auto_add_subtitle.utils.file_utils import write_srt_file


class CommonPresent:
    def __init__(self, view):
        self.view = view
        self.model = Model()

    def extract_audio(self, video_file, audio_file_path=None):
        if not audio_file_path:
            audio_file_path = os.path.join(os.path.dirname(video_file),
                                           "{}.wav".format(os.path.splitext(os.path.basename(video_file))[0]))
        extra_audio_and_transform(video_file, audio_file_path)
        return audio_file_path

    def transform_audio(self, audio_file, trans_audio_file_path=None):
        if not trans_audio_file_path:
            trans_audio_file_path = os.path.join(os.path.dirname(audio_file),
                                                 "{}_trans.wav".format(
                                                     os.path.splitext(os.path.basename(audio_file))[0]))
        extra_audio_and_transform(audio_file, trans_audio_file_path)
        return trans_audio_file_path

    def check_audio_should_trans(self, audio_file):
        with wave.open(audio_file, "r") as f:
            nchannels, sampwidth, framerate, nframes, comptype, compname = f.getparams()
            return sampwidth == 's16' and framerate == 16000

    def generate_subtitle(self, audio_file, srt_file):
        cut_result = cut_audio(audio_file)
        recognize_result = []
        for i in cut_result[0]:
            result = parse_audio_baidu(i[0], 16000)
            if not result:
                continue
            recognize_result.append((i[1], i[2], result[0]))
        # with open("result.json", 'r') as f:
        #     recognize_result = json.load(f)
        write_srt_file(srt_file, recognize_result)

    def combine_video_and_srt(self, video_file, srt_file):
        new_file_name = os.path.join(os.path.dirname(video_file),
                                     "{}_new{}".format(*os.path.splitext(os.path.basename(video_file))))
        combine_video_and_srt(video_file, srt_file, new_file_name)

    def process_file(self, file_path, is_audio):
        audio_file_path = os.path.join(os.path.dirname(file_path),
                                       "{}.wav".format(os.path.splitext(os.path.basename(file_path))[0]))
        if is_audio:
            if not self.check_audio_should_trans(file_path):
                trans_audio_file_path = os.path.join(os.path.dirname(file_path),
                                                     "{}_trans.wav".format(
                                                         os.path.splitext(os.path.basename(file_path))[0]))
                audio_file_path = self.transform_audio(file_path, trans_audio_file_path)
            else:
                audio_file_path = file_path
        else:
            self.extract_audio(file_path, audio_file_path)
        srt_file = os.path.join(os.path.dirname(audio_file_path),
                                "{}.srt".format(os.path.splitext(os.path.basename(audio_file_path))[0]))

        self.generate_subtitle(audio_file_path, srt_file)
        if not is_audio:
            self.combine_video_and_srt(file_path, srt_file)

    def start(self, *args, **kwargs):
        raise NotImplementedError()


def main():
    pass


if __name__ == "__main__":
    main()
