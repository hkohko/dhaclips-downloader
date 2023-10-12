def check_second(sec):
    if int(sec) < 60:
        return True
    return False


def check_minutes(mins):
    if int(mins) < 60:
        return True
    return False


def check_hours(hours):
    if int(hours) < 24:
        return True
    return False


def get_seconds(time_str):
    if ":" not in time_str:
        if check_second(time_str):
            return time_str
    unpack = time_str.split(":")
    print(unpack)
    if len(unpack) == 2:
        mm, ss = unpack
        if all((check_second(ss), check_minutes(mm))):
            return (int(mm) * 60) + int(ss)
    if len(unpack) == 3:
        hh, mm, ss = unpack
        if all((check_second(ss), check_minutes(mm), check_hours(hh))):
            return (int(hh) * 3600) + (int(mm) * 60) + int(ss)


if __name__ == "__main__":
    print(get_seconds("60"))
