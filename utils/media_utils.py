# coding:utf-8
import subprocess
import wave
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt

from auto_add_subtitle.utils.time_utils import seconds_to_timestamp_str


def get_wave_statistic(wave_data, framerate, threshhold=0.2):
    splitlist = []

    zerolen = 0
    nonezerolen = 0

    if wave_data[0] == 0:
        pre = -1
    else:
        pre = 0

    for v in wave_data:
        if (abs(v) <= threshhold and abs(pre) <= threshhold) or (abs(v) > threshhold and abs(pre) > threshhold):
            if abs(v) <= threshhold:
                zerolen += 1
                nonezerolen = 0
            else:
                nonezerolen += 1
                zerolen = 0
        elif abs(v) <= threshhold < abs(pre) or abs(v) > threshhold >= abs(pre):
            if abs(v) > threshhold:
                if len(splitlist) != 0:
                    zerolen += 1
                    nonezerolen = 0
                if zerolen > framerate * 17 - 1:
                    while zerolen > framerate * 17 - 1:
                        splitlist.append([False, framerate * 17 - 1, 0, 0, 0])
                        zerolen -= framerate * 17 - 1
                splitlist.append([False, zerolen, 0, 0, 0])
            else:
                if len(splitlist) != 0:
                    nonezerolen += 1
                    zerolen = 0
                splitlist.append([True, nonezerolen, 0, 0, 0])
        pre = v

    if zerolen:
        splitlist.append([False, zerolen, 0, 0, 0])
    if nonezerolen:
        splitlist.append([True, nonezerolen, 0, 0, 0])
    return splitlist


def plot_data(wave_data, nframes, framerate):
    time = np.arange(0, nframes) * (1.0 / framerate)
    fig = plt.figure(figsize=(100, 2))
    plt.plot(time, wave_data)
    plt.xlabel("Time(s)")
    plt.ylabel("Amplitude")
    plt.title("Single channel wavedata")
    plt.grid('on')  # 标尺，on：有，off:无。
    fig.savefig('test2png.png', dpi=100)


def timevalidate(timetable, endtime, timerange):
    timetable += [endtime]
    for i in range(len(timetable) - 1):
        if timetable[i + 1] - timetable[i] > timerange:
            return False
    return True


# 折半插入排序
def insertsort(timearr, item):
    if len(timearr) == 1:
        timearr.append(item) if item > timearr[0] else timearr.insert(0, item)
    elif len(timearr) == 2:
        if item > timearr[0]:
            timearr.append(item) if item > timearr[1] else timearr.insert(1, item)
        else:
            timearr.insert(0, item)
    else:
        if item < timearr[0]:
            timearr.insert(0, item)
        elif item > timearr[len(timearr) - 1]:
            timearr.append(item)
        else:
            middle(timearr, 0, len(timearr) - 1, item)


# 折半插入排序递归方法
def middle(timearr, start, end, item):
    if end - start == 1:
        timearr.insert(end, item)
    else:
        middle(timearr, start, (start + end) // 2, item) if timearr[(start + end) // 2] > item else middle(timearr, (
                start + end) // 2, end, item)


def time_transform(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("%02d:%02d:%02d" % (h, m, s))


def calculate_other_statistic_info(wavestatistic, framerate):
    id = 1
    sum = 0
    for record in wavestatistic:
        t = (sum + record[1] / 2.0) * 1 / framerate
        sum += record[1]
        record[2] = id
        record[3] = sum
        record[4] = t
        id += 1
        if record[1] > 2 * 17 * framerate:
            break


def load_wave(wave_path):
    with wave.open(wave_path, 'rb') as f:
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes, comptype, compname = params
        audio_frames = f.readframes(nframes)  # 读取音频，字符串格式
        return nchannels, sampwidth, framerate, nframes, audio_frames


def process_audio_data(audio_frames, frames, channels):
    wave_data = np.fromstring(audio_frames, dtype=np.int16)

    # 中值滤波medfilt计算太慢,使用下面方法速度提升一倍
    # wave_data=signal.medfilt(wave_data)
    middata = [0] * len(wave_data)
    if len(wave_data) > 2:
        middata[0] = sorted([0, wave_data[1], wave_data[2]])[1]
        middata[len(wave_data) - 1] = sorted([0, wave_data[len(wave_data) - 1], wave_data[len(wave_data) - 2]])[1]
    for i in range(1, len(wave_data) - 1):
        middata[i] = (wave_data[i] if wave_data[i] > wave_data[i + 1] else \
                          (wave_data[i + 1] if wave_data[i - 1] > wave_data[i + 1] else wave_data[i - 1])) \
            if wave_data[i - 1] > wave_data[i] else \
            (wave_data[i - 1] if wave_data[i - 1] > wave_data[i + 1] else \
                 (wave_data[i + 1] if wave_data[i] > wave_data[i + 1] else wave_data[i]));
    for j in range(len(wave_data)):
        wave_data[j] = middata[j]

    # wave幅值归一化 取数组中最大的值为分母,每个元素作为分母
    wave_data = wave_data * 1.0 / (max(abs(wave_data)))
    if channels > 1:
        wave_data = np.reshape(wave_data, [frames, channels])
        wave_data = wave_data[:, 0]
    return wave_data


def sort_split_data(sortedwavestatistic, frames, frame_rate):
    splittimestamp = [0]
    for split in sortedwavestatistic:
        # split[4]为音频时间点,表示到目前时长总长,单位为s
        # 插入并折半排序
        insertsort(splittimestamp, split[4])
        # nframes字节总长度/采样率
        # print(nframes*1.0/8000); 输出329.537625等于5分29秒,如果相邻2段都小于17秒则结束
        if timevalidate(splittimestamp, frames * 1.0 / frame_rate, 17):
            break
        splittimestamp.pop()
    return splittimestamp


def cut_audio(wave_path):
    channels, samp_width, frame_rate, frames, audio_frames = load_wave(wave_path)
    # 使用字符串创建矩阵,简单的转换实现了ASCII码的转换,int16使得每2个字符(16位)转化成10进制的数组

    wave_data = process_audio_data(audio_frames, frames, channels)
    # plot_data(wave_data,nframes,framerate)#绘制音频波谱图片
    # 统计有声音和没声音的分段每段时长
    wavestatistic = get_wave_statistic(wave_data, frame_rate)
    calculate_other_statistic_info(wavestatistic, frame_rate)

    sortedwavestatistic = sorted(wavestatistic, key=lambda x: (x[0], -x[1]))
    splittimestamp = sort_split_data(sortedwavestatistic, frames, frame_rate)

    wav = AudioSegment.from_wav(wave_path)  # 打开mp3文件
    cut_results = []
    for i in range(len(splittimestamp) - 1):
        starttime = splittimestamp[i]
        endtime = splittimestamp[i + 1]
        if endtime > frames * 1.0 / frame_rate:
            endtime = frames * 1.0 / frame_rate
        cut_bytes = wav[starttime * 1000:endtime * 1000].raw_data
        startstr = seconds_to_timestamp_str(starttime)
        endstr = seconds_to_timestamp_str(endtime)
        cut_results.append((cut_bytes, startstr, endstr))
    return cut_results, frame_rate, samp_width


def main():
    result = cut_audio(r"C:\Users\Administrator\Downloads\AutosubBehindWall-master\dataset\ted80001.wav")
    for i in result[0]:
        print(i[1], i[2])


if __name__ == "__main__":
    main()
