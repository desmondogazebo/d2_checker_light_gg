import time


def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def get_new_unix_timestamp(sec_elapse):
    curr_ts = round(time.time())
    return sec_elapse + curr_ts
