import os
from tkmail.tkmail import Email


def send_email(email_config, content=''):
    if 'files' in email_config:
        files = []
        for path in email_config:
            path = os.path.abspath(path)
            if os.path.exists(path) and os.path.isfile(path):
                files.append(path)
        email_config['files'] = files
  
    email = Email('smtp.gmail.com', 587, email_config['smtp']['username'], email_config['smtp']['pwd'])
    email.send_mail(
        '{} <{}>'.format(email_config['from'], email_config['smtp']['username']),
        email_config['to'],
        email_config['subject'],
        content,
        cc=email_config.get('cc', []),
        bcc=email_config.get('bcc', []),
        files=email_config.get('files'),
    )
