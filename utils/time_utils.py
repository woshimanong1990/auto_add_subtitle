# coding:utf-8


def seconds_to_timestamp_str(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    timestamp = ("%02d:%02d:%06.3f" % (h, m, s))
    return timestamp


def main():
    pass


if __name__ == "__main__":
    main()
