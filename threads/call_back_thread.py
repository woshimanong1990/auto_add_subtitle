# coding:utf-8
from PySide2.QtCore import QThread, Signal
from utils.variables import LOGGER


class CallBackThread(QThread):
    done_signal = Signal(object, bool)

    def __init__(self, func, *args, **kwargs):
        super(CallBackThread, self).__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.done_signal.emit(result, False)
        except Exception as e:
            LOGGER.error("process err", exc_info=True)
            self.done_signal.emit(e, True)


def main():
    pass


if __name__ == "__main__":
    main()
