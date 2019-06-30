import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


context = ssl.create_default_context()
def send_mail(send_from, send_to, subject, text, files=None,
              server="auto find", port=25):
    assert isinstance(send_to, list)
    if server == 'auto find':
        server = 'smtp.' + send_to.split('@')[-1]
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)


    smtp = smtplib.SMTP(server, port)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()
