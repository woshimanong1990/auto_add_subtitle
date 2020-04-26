# coding:utf-8
from threads.call_back_thread import CallBackThread


class Model:
    def __init__(self):
        self.thread = None

    def start(self, call_back, func, *args, **kwargs):
        self.thread = CallBackThread(func, *args, **kwargs)
        self.thread.done_signal.connect(call_back)
        self.thread.start()


def main():
    pass


if __name__ == "__main__":
    main()
