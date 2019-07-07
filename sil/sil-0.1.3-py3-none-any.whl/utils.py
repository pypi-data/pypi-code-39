import datetime

def estimate_time_remaining(prev_time, curr_time, steps_between, current_step, total_steps):
    remaining_steps = total_steps - current_step
    time_elapsed = curr_time - prev_time
    if steps_between == 0:
        time_elapsed_per_step = datetime.timedelta(seconds=0)
    else:
        time_elapsed_per_step = time_elapsed / steps_between
    time_remaining = remaining_steps * time_elapsed_per_step
    return datetime.timedelta(seconds=time_remaining.seconds)
