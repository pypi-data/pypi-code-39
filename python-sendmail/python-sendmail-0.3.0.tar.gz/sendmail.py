# -*- coding: utf-8 -*-
import os
import io
from io import open
import smtplib
from email import generator
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
from email.parser import Parser
import mimetypes
import click


def ignore_default_codec_map():
    from email import charset
    _names = list(charset.CODEC_MAP.keys())
    for _name in _names:
        del charset.CODEC_MAP[_name]


def get_content(content, encoding="utf-8"):
    if not content:
        if hasattr(os.sys.stdin, "reconfigure"):
            os.sys.stdin.reconfigure(encoding=encoding)
            content = os.sys.stdin.read()
            return content
        else:
            import codecs
            content = codecs.getreader(encoding)(os.sys.stdin).read()
            return content
    if os.path.exists(content):
        with open(content, "r", encoding=encoding) as fobj:
            return fobj.read()
    return content


def addresses_encode(addresses, charset="utf-8"):
    return ", ".join([address_encode(address, charset) for address in addresses])


def address_encode(value, charset="utf-8"):
    if u"<" in value:
        name, email = value.split(u"<")
        name = name.strip()
        email = email.replace(u">", u"")
    else:
        name = value
        email = value
    return u"{0} <{1}>".format(header_encode(name, charset), email)


def header_encode(value, charset="utf-8"):
    return Header(value, charset).encode()


def get_smtp_service(host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    if ssl:
        smtp_service = smtplib.SMTP_SSL(host, port)
    else:
        smtp_service = smtplib.SMTP(host, port)
    if user and password:
        smtp_service.login(user, password)
    return smtp_service


def get_message_from_eml_content(content):
    parser = Parser()
    return parser.parsestr(content)


def make_message(from_address, to_addresses, content, subject, attachs=None, is_html_content=False, charset="utf-8"):
    message = MIMEMultipart()
    if subject:
        message["Subject"] = header_encode(subject, charset)
    message["From"] = address_encode(from_address, charset)
    message["To"] = addresses_encode(to_addresses, charset)

    if is_html_content:
        main_content = MIMEText(content, "html", charset)
    else:
        main_content = MIMEText(content, "plain", charset)
    message.attach(main_content)

    attachs = attachs or []
    for attach in attachs:
        basename = header_encode(os.path.basename(attach), charset)
        part = None
        with open(attach, "rb") as attach_file:
            part = MIMEApplication(attach_file.read(), Name=basename)
        part.add_header("Content-Disposition", "attachment", filename=basename)
        message.attach(part)

    return message


def makemail(from_address, to_addresses, subject, attach, html, encoding, charset, output, content):
    content = get_content(content, encoding)
    message = make_message(from_address, to_addresses, content, subject, attach, html, charset)
    buffer = io.StringIO()
    gen = generator.Generator(buffer)
    gen.flatten(message)
    if output:
        with open(output, "w") as fobj:
            fobj.write(buffer.getvalue())
    else:
        click.echo(buffer.getvalue())
    return message


def sendmail(from_address, to_addresses, content, subject, attachs=None, is_html_content=False, encoding="utf-8", charset="utf-8", host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    content = get_content(content, encoding)
    smtp_service = get_smtp_service(host, port, ssl, user, password)
    message = make_message(from_address, to_addresses, content, subject, attachs, is_html_content, charset)
    smtp_service.send_message(message)
    smtp_service.quit()


def sendeml(content, encoding="utf-8", host="127.0.0.1", port=25, ssl=False, user=None, password=None):
    content = get_content(content, encoding)
    smtp_service = get_smtp_service(host, port, ssl, user, password)
    message = get_message_from_eml_content(content)
    smtp_service.send_message(message)
    smtp_service.quit()


@click.group()
def main():
    """提供邮件发送相关函数及可执行程序。


注意：


1、如果可执行参数中没有提供邮件内容，则表示从STDIN中获取邮件内容。

2、如果可执行参数中提供的邮件内容是一个文件，则读取文件内容作为邮件内容。

3、其它情况则将可执行参数中提供的邮件内容作为邮件正文内容。
    """
    pass


@main.command(name="makemail")
@click.option("-f", "--from-address", required=True, help=u"发件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-t", "--to-address", multiple=True, required=True, help=u"收件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-s", "--subject", help=u"邮箱主题。")
@click.option("-a", "--attach", multiple=True, required=False, help=u"邮件附件，可以使用多次。")
@click.option("--html", is_flag=True, help=u"使用HTML格式。")
@click.option("-e", "--encoding", default="utf-8", help=u"STDIN中邮件内容的字符编码，默认为UTF-8。")
@click.option("-c", "--charset", default="utf-8", help=u"发送时邮件内容的编码，默认为UTF-8。")
@click.option("-o", "--output", required=False, help=u"生成邮件的保存位置。")
@click.argument("content", nargs=1, required=False)
def makemail_cmd(from_address, to_address, subject, attach, html, encoding, charset, output, content):
    """生成EML格式邮件。
    """
    ignore_default_codec_map()
    to_addresses = to_address
    makemail(from_address, to_addresses, subject, attach, html, encoding, charset, output, content)


@main.command(name="sendmail")
@click.option("-f", "--from-address", required=True, help=u"发件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-t", "--to-address", multiple=True, required=True, help=u"收件人，如：姓名 <name@example.com>、name@example.com。")
@click.option("-s", "--subject", help=u"邮箱主题。")
@click.option("-a", "--attach", multiple=True, required=False, help=u"邮件附件，可以使用多次。")
@click.option("--html", is_flag=True, help=u"使用HTML格式。")
@click.option("-e", "--encoding", default="utf-8", help=u"STDIN中邮件内容的字符编码，默认为UTF-8。")
@click.option("-c", "--charset", default="utf-8", help=u"发送时邮件内容的编码，默认为UTF-8。")
@click.option("-h", "--host", default="127.0.0.1", help=u"邮箱代理服务器地址，默认为127.0.0.1。")
@click.option("-p", "--port", default=25, help=u"邮箱代理服务器端口，默认为25。")
@click.option("--ssl", is_flag=True, help=u"邮箱代理服务器要求使用ssl加密链接。")
@click.option("-u", "--user", help=u"邮箱代理服务器帐号，不提供则表示无需帐号认证。")
@click.option("-P", "--password", help=u"邮箱代理服务器密码，不提供则表示无需帐号认证。")
@click.argument("content", nargs=1, required=False)
def sendmail_cmd(from_address, to_address, subject, attach, html, encoding, charset, host, port, ssl, user, password, content):
    u"""通过代理服务器发送邮件。
    """
    ignore_default_codec_map()
    to_addresses = to_address
    sendmail(from_address, to_addresses, content, subject, attach, html, encoding, charset, host, port, ssl, user, password)


@main.command(name="sendeml")
@click.option("-h", "--host", default="127.0.0.1", help=u"邮箱代理服务器地址，默认为127.0.0.1。")
@click.option("-p", "--port", default=25, help=u"邮箱代理服务器端口，默认为25。")
@click.option("--ssl", is_flag=True, help=u"邮箱代理服务器要求使用ssl加密链接。")
@click.option("-u", "--user", help=u"邮箱代理服务器帐号，不提供则表示无需帐号认证。")
@click.option("-P", "--password", help=u"邮箱代理服务器密码，不提供则表示无需帐号认证。")
@click.option("-e", "--encoding", default="utf-8", help=u"STDIN中邮件内容的字符编码，默认为UTF-8。")
@click.argument("content", nargs=1, required=False)
def sendeml_cmd(host, port, ssl, user, password, encoding, content):
    u"""通过代理服务器发送EML格式邮件。
    """
    sendeml(content, encoding, host, port, ssl, user, password)


if __name__ == "__main__":
    main()
