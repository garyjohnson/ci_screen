import time


def eventually(condition, retries=6, loop_delay=0.5):
    met_condition = False
    for i in range(0, retries):
        time.sleep(loop_delay)
        met_condition = condition()
        if met_condition:
            break

    return met_condition


def consistently(condition, retries=6, loop_delay=0.5):
    for i in range(0, retries):
        time.sleep(loop_delay)
        met_condition = condition()
        if not met_condition:
            return False

    return True
