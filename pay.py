MINUTES_PER_DAY = 1440


def time_to_minutes(time_text):
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def is_ooh(clock_time, ooh_start, ooh_end):
    if ooh_start > ooh_end:
        return clock_time >= ooh_start or clock_time < ooh_end
    return ooh_start <= clock_time < ooh_end


def split_minutes(start_time, end_time, ooh_start_time, ooh_end_time):
    start = time_to_minutes(start_time)
    end = time_to_minutes(end_time)
    ooh_start = time_to_minutes(ooh_start_time)
    ooh_end = time_to_minutes(ooh_end_time)

    if end <= start:
        end += MINUTES_PER_DAY

    day_minutes = 0
    ooh_minutes = 0
    for minute in range(start, end):
        if is_ooh(minute % MINUTES_PER_DAY, ooh_start, ooh_end):
            ooh_minutes += 1
        else:
            day_minutes += 1

    return day_minutes, ooh_minutes


def calculate_earnings(
    start_time, end_time, ooh_start_time, ooh_end_time, day_rate, ooh_rate
):
    day_minutes, ooh_minutes = split_minutes(
        start_time, end_time, ooh_start_time, ooh_end_time
    )
    return day_minutes / 60 * day_rate + ooh_minutes / 60 * ooh_rate
