# coding:utf-8
from auto_add_subtitle.utils.variables import LOGGER


def error_capture_wrapper(error_value=None):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                LOGGER.error("%s run error", func.__name__, exc_info=True)
                return error_value
        return wrapped
    return wrapper

def main():
    pass


if __name__ == "__main__":
    main()
