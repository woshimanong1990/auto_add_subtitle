# coding:utf-8
import os
import json
import sys

from auto_add_subtitle.utils.logger_utils import error_capture_wrapper


def get_root_dir(is_relative_to_execute=False):
    if getattr(sys, 'frozen', False):
        if is_relative_to_execute:
            return os.path.dirname(sys.executable)
        else:
            return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_file_path(path, is_relative_to_execute=False):
    root_dir = get_root_dir(is_relative_to_execute=is_relative_to_execute)
    basename = os.path.basename(path)
    if getattr(sys, 'frozen', False):
        return os.path.join(root_dir, basename)
    else:
        return os.path.join(root_dir, path)


@error_capture_wrapper(error_value={})
def get_settings():
    settings_path = get_file_path('data/settings.json', is_relative_to_execute=True)
    if not os.path.isfile(settings_path):
        return {}
    with open(settings_path, "r") as f:
        return json.load(f)


def get_baidu_settings():
    data = get_settings()
    baidu_app_id = data.get("baidu_app_id", None)
    baidu_api_key = data.get("baidu_api_key", None)
    baidu_secret = data.get("baidu_secret", None)
    return baidu_app_id, baidu_api_key, baidu_secret


def write_srt_file(file_path, srt_data):
    srttxt = ''
    for i, data in enumerate(srt_data):
        reorganize_txt = "\n".join([data[2][i:i+30] for i in range(0, len(data[2]), 30)])
        srttxt += '%s\n%s --> %s\n%s\n\n' % (i + 1, data[0], data[1], reorganize_txt)
    with open(file_path, 'wb') as f:
        f.write(srttxt.encode("utf-8"))


def get_ffmpeg_file_path():
    return get_file_path('data/ffmpeg.exe')


def get_probe_file_path():
    return get_file_path('data/ffprobe.exe')


def main():
    pass


if __name__ == "__main__":
    main()
