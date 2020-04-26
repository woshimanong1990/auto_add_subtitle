# coding:utf-8

from presents.common_present import CommonPresent


class AddSubtitlePresent(CommonPresent):
    def start(self, video, srt):
        self.model.start(self.view.show_result, self.combine_video_and_srt, video, srt)


def main():
    pass


if __name__ == "__main__":
    main()
