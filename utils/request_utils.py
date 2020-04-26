# coding:utf-8
from aip import AipSpeech
from auto_add_subtitle.utils.logger_utils import error_capture_wrapper
from auto_add_subtitle.utils.file_utils import get_baidu_settings


def parse_audio_baidu(filestream, samplerate):
    aip_speech = AipSpeech(*get_baidu_settings())
    response = aip_speech.asr(filestream, 'wav', samplerate, {
        # 'lan': language,
        'dev_pid': 1537,
    })
    if response.get("err_no") != 0:
        return []
    return response.get('result')


def main():
    pass


if __name__ == "__main__":
    main()
