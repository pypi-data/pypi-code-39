# coding: utf-8

"""
the code passed test with aliyun email and aliyun ecs
适用于部署在阿里云服务器
"""

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Tuple, Union


class Email:

    def __init__(self, mail_user: str, mail_pass: str, sender: str = None, mail_host: str = 'smtp.mxhichina.com',
                 port=465):
        """

        :param mail_user: 用户
        :param mail_pass: 密码
        :param sender:
        :param mail_host:
        :param port:
        """
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_pass = mail_pass
        # 启用SSL发信, 端口一般是465, 22 端口阿里云服务器默然禁掉
        self.port = port
        self.debuglevel = 2
        self.sender = sender if self.sender else self.mail_user

    def update_message(self, message, sender: str, receivers: str, title: str):
        message['From'] = sender
        message['To'] = ",".join(receivers) if isinstance(receivers, (list, tuple)) else receivers
        message['Subject'] = title
        return message

    def upload_file(self, filename: str):
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            if filename.find('/') != -1:
                filename = os.path.split(filename)[-1]
            part.add_header('content-disposition', 'attachment', filename=filename)
            return part

    def _send_email(self, receivers: str, message: str):
        smtpObj = smtplib.SMTP_SSL(self.mail_host, self.port)
        smtpObj.login(self.mail_user, self.mail_pass)
        smtpObj.set_debuglevel(self.debuglevel)
        smtpObj.sendmail(self.sender, receivers, message)
        smtpObj.quit()

    def send_email(self, title: str, content: str, receivers: Union[Tuple[str], str],
                   subtype: str = 'html') -> None:
        # 内容, 格式, 编码
        message = MIMEText(content, subtype, 'utf-8')
        message = self.update_message(message, self.sender, receivers, title)
        self._send_email(receivers, message.as_string())

    def send_email_attach(self, title: str, content: str, filename: str, receivers: Union[Tuple[str], str],
                          subtype: str = 'html'):
        message = MIMEMultipart()  # 内容, 格式, 编码
        message = self.update_message(message, self.sender, receivers, title)
        message.attach(MIMEText(content, subtype, 'utf-8'))
        # Add attachment to message and convert message to string
        message.attach(self.upload_file(filename))
        self._send_email(receivers, message.as_string())
