# coding:utf-8
import json

from auto_add_subtitle.utils.media_utils import cut_audio
from auto_add_subtitle.utils.request_utils import parse_audio_baidu
from auto_add_subtitle.utils.file_utils import write_srt_file
from auto_add_subtitle.utils.process_utils import extra_audio_and_transform, combine_video_and_srt

def main():
    # file_path = r'D:\myCode\python\testCode\add_subtitle\data\test.wav'
    # cut_result = cut_audio(file_path)
    # recognize_result = []
    # for i in cut_result[0]:
    #     result = parse_audio_baidu(i[0], 16000)
    #     if not result:
    #         continue
    #     recognize_result.append((i[1], i[2], result[0]))
    with open("result.json", 'r') as f:
        recognize_result = json.load(f)
    write_srt_file("result1.srt", recognize_result)


if __name__ == "__main__":
    main()
