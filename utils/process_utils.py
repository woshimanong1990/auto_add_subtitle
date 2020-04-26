# coding:utf-8
import os
import subprocess

from auto_add_subtitle.utils.file_utils import get_ffmpeg_file_path, get_probe_file_path
from auto_add_subtitle.utils.variables import LOGGER


def subprocess_args(include_stdout=True):
    if hasattr(subprocess, 'STARTUPINFO'):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None
    if include_stdout:
        ret = {'stdout': subprocess.PIPE}
    else:
        ret = {}
    ret.update({'stdin': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'startupinfo': si,
                'env': env})
    return ret


def extra_audio_and_transform(file_path, audio_file_path):
    ffmpeg = get_ffmpeg_file_path()
    FNULL = open(os.devnull, 'w')
    LOGGER.info("start extra audio")
    # stdout=FNULL,
    subprocess.check_call([ffmpeg, "-i", file_path, "-ac", '1',  '-ar', '16000',
                           '-acodec', "pcm_s16le",
                           '-f', 'wav', '-vn', '-y', audio_file_path],
                          stdout=FNULL,
                          stderr=subprocess.STDOUT
                          )
    LOGGER.info("extra audio done")


def replace_srt_file_path(srt_file):
    drive, tail = os.path.splitdrive(os.path.normpath(srt_file).replace("\\\\", "/"))
    tail = tail.replace("\\", "/")
    return "{}\\:{}".format(drive[0], tail)


def extract_video_bit_rate(video_path):
    try:
        ffprobe = get_probe_file_path()
        result = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                                 "format=bit_rate", "-of",
                                 "default=noprint_wrappers=1:nokey=1", video_path],
                                **subprocess_args(True))
        return int(result.stdout.strip())
    except:
        LOGGER.error("get video bit rate error %s", video_path, exc_info=True)
        return 2 * 1024 * 1024


def extract_video_duration(video_path):
    try:
        ffprobe = get_probe_file_path()
        result = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", video_path],
                                **subprocess_args(True))
        return float(result.stdout.strip())
    except:
        LOGGER.error("get video duration error %s", video_path, exc_info=True)
        return None


def combine_video_and_srt(video_file, srt_file, new_file_path=None):
    if new_file_path is None:
        new_file_path = os.path.join(os.path.dirname(video_file),
                                     "{}_new{}".format(*os.path.splitext(os.path.basename(video_file))))

    ffmpeg = get_ffmpeg_file_path()
    new_srt_file = replace_srt_file_path(srt_file)
    bit_rate = extract_video_bit_rate(video_file)
    call_ = [ffmpeg, "-i", video_file, "-filter_complex", r"subtitles='{}'".format(new_srt_file),
             '-c:a', "copy",
             "-b:v", str(bit_rate),
             "-bufsize", "1M",
             "-y", new_file_path]
    FNULL = open(os.devnull, 'w')
    subprocess.check_call(call_, stdout=FNULL, stderr=subprocess.STDOUT)


def main():
    pass


if __name__ == "__main__":
    main()
