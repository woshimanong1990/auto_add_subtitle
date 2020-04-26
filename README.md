自动加载字幕

# 原理
将音频按照空白分割，每个音频片段使用百度语音识别转成文字，最终将结果输出到srt

# 软件使用说明
软件提供音频输出字幕，以及视频自动添加字幕并输出。视频还会在同目录下输出srt

![img](res\images\detail.png)

## 功能说明

### 仅音频

根据百度的要求，音频会被转成：单声道，s16，16000 rate这样一种格式，不符合的自动转换.转换的文件名：file_name_trans.wav

输出的字幕文件名：file_name.srt

### 视频

先提取音频并转成符合百度的格式（同上），自动合成字幕。新的视频名称：file_name_new.mp4

所有的输出文件都在源文件目录下
-------

### 工具说明

#### 提取音频
选择需要提取的视频，并选择需要目标文件夹。提取的视频格式同上

### 转换音频
选择需要提取的音频，并选择需要目标文件夹，最后的格式是百度需要的

### 合成字幕
提供视频和srt字幕文件，合成新的视频

# 使用说明

依赖的库，在requirements.txt列出
去 [百度ai](https://ai.baidu.com/) 申请账号，并创建应用。将baidu_app_id, baidu_api_key, baidu_secret填入data/settings.json中

对于exe，填入exe所在目录中的settings.json

# 说明

1 处理时间取决于文件大小和网络，请耐心等待

2 音频识别结果可能有出入，可以自行修改

3 请勿商用

# exe link
链接: https://pan.baidu.com/s/1Shpsik5M4uK_kgP04KNePw 提取码: vgki

# todo

0 添加注释

1 多语言支持

2 多api支持

3 加快处理速度

4 字幕样式支持

5 字幕编辑支持

6 基础版和pro版

# more thing

like it, star  it ; )




