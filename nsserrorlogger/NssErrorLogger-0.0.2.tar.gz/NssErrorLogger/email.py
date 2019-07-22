import datetime
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage

class SMTPConfig:
    host = "smtp.126.com"
    user = "tk_info"
    passwd = "asdfg123"


def logMsg(module, subject, msg):
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = Address(module+" Message", "tk_info", "126.com")
    message['To'] = Address("", "tk_info", "126.com")

    msg = "%s, %s: \n%s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), module, msg)
    message.set_content(msg)

    try:            
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(SMTPConfig.host, 25)
        smtpObj.login(SMTPConfig.user, SMTPConfig.passwd)
        smtpObj.sendmail(message["From"], message["To"], message.as_string())
    except Exception as e:
        with open("error.log", "a+") as f:
            f.write("[%s] %s: Send msg %s - %s Failed due to:\n" % (module, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), subject, msg))
            f.write("\t[NssErrorLogger] %s: Generate error %s\n" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), e))
