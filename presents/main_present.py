# coding:utf-8
from presents.common_present import CommonPresent


class MainPresent(CommonPresent):
    def start(self, file_path, is_audio):
        self.model.start(self.view.show_result, self.process_file, file_path, is_audio)


def main():
    pass


if __name__ == "__main__":
    main()
