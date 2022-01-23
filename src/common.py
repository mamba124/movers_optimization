import os


def validate_launch_time():
    start = os.environ.get("START")
    finish = os.environ.get("FINISH")
    if not start:
        start = 16
    if not finish:
        finish = 8
    start_time = int(start)
    finish_time = int(finish)
    return start_time, finish_time