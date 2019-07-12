import time

def console_log(check, success):
    TEMPLATE = """
!!! {check_name} {status} !!!
Reported at {cur_time} ({cur_date}).
{message}

"""

    if success:
        status = "RECOVERY"
        error_message = check.recovery
    else:
        status = "FAILURE"
        error_message = check.failure

    print(TEMPLATE.format(
        check_name=check.name,
        status=status,
        cur_time=time.strftime("%H:%M:%S"),
        cur_date=time.strftime("%d %b %Y"),
        message=error_message,
    ))