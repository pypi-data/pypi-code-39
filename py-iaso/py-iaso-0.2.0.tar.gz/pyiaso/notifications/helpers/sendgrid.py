import time
from socket import gethostname
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Tuple

from .. import raise_invalid_key, raise_missing_key, print_log

def email_sendgrid(check, success: bool, **kwargs):
    if "api_key" not in kwargs.keys() and "recipients" not in kwargs.keys():
        raise_invalid_key('email_sendgrid')

    subject, message = create_email(check, success, kwargs['recipients'], kwargs.get('subject_prefix', None))
    
    message = Mail(
        from_email='timoguic@gmail.com',
        to_emails=kwargs['recipients'],
        subject=subject,
        html_content=message,
    )

    try:
        sg = SendGridAPIClient(kwargs['api_key'])
        response = sg.send(message)
        if 200 <= response.status_code < 300:
            print_log('Mail sent to', *kwargs['recipients'])
    except Exception as e:
        print(str(e))

def create_email(check, success, recipients, subject_prefix=None) -> Tuple[str]:

    MAIL_TEMPLATE = """
    <h1>{check_name} {status}</h1>
    <h2>Reported on <strong>{host}</strong> at {cur_time} ({cur_date}).</h2>
    <p>Message:</p>
    <pre>{message}</pre>
    """

    if success:
        status = "RECOVERY"
        error_message = check.recovery
    else:
        status = "FAILURE"
        error_message = check.failure

    prefix = subject_prefix + ' ' if subject_prefix else subject_prefix
    
    subject = "{} {} {}".format(prefix, check.name, status)
    message = MAIL_TEMPLATE.format(
        check_name=check.name,
        status=status,
        cur_time=time.strftime("%H:%M:%S"),
        cur_date=time.strftime("%d %b %Y"),
        host=gethostname(),
        message=error_message,
    )

    return subject, message