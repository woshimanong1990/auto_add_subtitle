# coding:utf-8

from auto_add_subtitle.utils.process_utils import extra_audio_and_transform
from auto_add_subtitle.utils.process_utils import combine_video_and_srt, extract_video_bit_rate


def main():
    video_file = r'test2222.mp4'
    # extra_file_from_video(video_file)
    subtitle_file = r'result1.srt'
    combine_video_and_srt(video_file, subtitle_file)
    # extract_video_bit_rate(video_file)


if __name__ == "__main__":
    main()
