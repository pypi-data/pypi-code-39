# -*- coding: utf-8 -*-
import os
from io import open
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import mimetypes
import click


def get_smtp_service(host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    if ssl:
        smtp_service = smtplib.SMTP_SSL(host, port)
    else:
        smtp_service = smtplib.SMTP(host, port)
    if user and password:
        smtp_service.login(user, password)
    return smtp_service


def get_message(from_address, to_address, content, subject, attachs=None, is_html_content=False, content_encoding="utf-8"):
    message = MIMEMultipart()
    if subject:
        message["Subject"] = subject
    message["From"] = from_address
    message["To"] = to_address

    if is_html_content:
        main_content = MIMEText(content, "html", content_encoding)
    else:
        main_content = MIMEText(content, "plain", content_encoding)
    message.attach(main_content)

    attachs = attachs or []
    for attach in attachs:
        basename = None
        part = None
        with open(attach, "rb") as attach_file:
            basename = os.path.basename(attach)
            part = MIMEApplication(attach_file.read(), Name=basename)
        part.add_header('Content-Disposition', 'attachment', filename=basename)
        message.attach(part)

    return message


def sendmail(from_address, to_address, content, subject, attachs=None, is_html_content=False, content_encoding="utf-8", host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    smtp_service = get_smtp_service(host, port, ssl, user, password)
    message = get_message(from_address, to_address, content, subject, attachs, is_html_content, content_encoding)
    if hasattr(smtp_service, "send_message"):
        smtp_service.send_message(message) # Python 2.7 or 3.x 
    else:
        smtp_service.sendmail(from_address, to_address, message.to_string()) # Python 2.6
    smtp_service.quit()


@click.command()
@click.option("-f", "--from-address", required=True, help=u"发件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-t", "--to-address", required=True, help=u"收件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-s", "--subject", help=u"邮箱主题。")
@click.option("-a", "--attach", multiple=True, required=False, help=u"邮件附件，可以使用多次。")
@click.option("--html", is_flag=True, help=u"使用HTML格式。")
@click.option("-e", "--encoding", default="utf-8", help=u"邮件内容编码格式，默认为UTF-8。")
@click.option("-h", "--host", default="127.0.0.1", help=u"邮箱代理服务器地址，默认为127.0.0.1。")
@click.option("-p", "--port", default=25, help=u"邮箱代理服务器端口，默认为25。")
@click.option("--ssl", is_flag=True, help=u"邮箱代理服务器要求使用ssl加密链接。")
@click.option("-u", "--user", help=u"邮箱代理服务器帐号，不提供则表示无需帐号认证。")
@click.option("-P", "--password", help=u"邮箱代理服务器密码，不提供则表示无需帐号认证。")
@click.argument("content", nargs=1, required=False)
def main(from_address, to_address, subject, content, attach, html, encoding, host, port, ssl, user, password):
    """通过代理服务器发送邮件。
    
    注意： 
    
    如果命令行中没有提供邮件内容，则表示从STDIN中获取邮件内容。
    """
    if not content:
        content = os.sys.stdin.read()
    sendmail(from_address, to_address, content, subject, attach, html, encoding, host, port, ssl, user, password)
    click.echo("邮件发送成功。主题：[{subject}]，发件人：[{from_address}]，收件人：[{to_address}]。".format(
        subject=subject or "(no subject)",
        from_address=from_address,
        to_address=to_address
        ))


if __name__ == "__main__":
    main()
