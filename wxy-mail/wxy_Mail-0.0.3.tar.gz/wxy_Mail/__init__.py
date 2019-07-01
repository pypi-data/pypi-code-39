import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import re




# 提取文件路径中的文件名
def file_name(path):
    '''
    提取文件路径中的文件名称
    :param path:文件路径
    :return:文件名称
    '''
    reg = r'([^<>/\\\|:""\*\?]+\.\w+$)'
    result = re.compile(reg).findall(path)[0]
    return result

class Mail:

    RECEIVER=None           # list
    SUBJECT=None            # str
    CONTENT=None            # str
    TYPE=None               # str
    ATTACHMENT_PATH=None    # list

    def __init__(self,user,password):
        '''
        user：发送人邮箱
        password：邮箱密码，若qq邮箱，则为授权码
        '''

        self.user = user
        self.password = password
        # 根据邮箱判断服务器

        smtp_sever={
            'fulaan':'smtp.exmail.qq.com',
            'qq':'smtp.qq.com',
            '163':'smtp.exmail.qq.com',
            '126':'smtp.126.com',
            '188':'smtp.188.com',
            'netease':'smtp.netease.com',
            'yeah':'smtp.yeah.net',
            'gmail':'smtp.gmail.com',
        }

        reg = r"@(.+?).com"
        try:
            result = re.compile(reg).findall(user)[0]
        except:
            raise Exception('无法识别邮箱名')

        try:
            self.host=smtp_sever[result]
        except:
            raise Exception('邮箱暂不支持自动发送')

    def add_receivers(self,receivers:list):
        '''
        receivers:邮件接收者  list
        '''
        if isinstance(receivers,list) is False:
            raise Exception('请传入list形式的receivers')
        Mail.RECEIVER=receivers

    def add_subject(self,subject:str):
        '''
        subject: 邮件主题
        '''
        if isinstance(subject,str) is False:
            raise Exception('请传入字符串形式的subject')
        Mail.SUBJECT=subject

    def add_content(self,type:str,content:str):
        '''
        content: 邮件正文
        type：正文格式     plain or html
        '''
        Mail.TYPE=type
        Mail.CONTENT=content

    def add_attachment(self,path):
        '''
        path: 邮件正文  list
        '''
        if isinstance(path,list) is False:
            raise Exception('请传入list形式的path')
        Mail.ATTACHMENT_PATH=path

    def send(self):

        To = ','.join(Mail.RECEIVER)      # 发给谁，默认填写发件人邮箱
        From = 'Auto-Mail'                # 谁发的

        # 不添加附件
        if Mail.ATTACHMENT_PATH == None:
            message = MIMEText(Mail.CONTENT, Mail.TYPE, 'utf-8')  # 创建一个不带附件的实例，加入正文
            message['Subject'] = Header(Mail.SUBJECT, 'utf-8')  # 加入标题
            message['From'] = Header(From, 'utf-8')  # 加入From
            message['To'] = Header(To, 'utf-8')  # 加入To
        # 添加附件
        else:
            message = MIMEMultipart()  # 构造一个带附件的实例
            message.attach(MIMEText(Mail.CONTENT, Mail.TYPE, 'utf-8'))  # 加入正文
            message['Subject'] = Header(Mail.SUBJECT, 'utf-8')  # 加入标题
            message['From'] = Header(From, 'utf-8')  # 加入From
            message['To'] = Header(To, 'utf-8')  # 加入To

            # 构造附件
            for i in Mail.ATTACHMENT_PATH:
                attachment_add = MIMEText(open('{}'.format(i), 'rb').read(), 'base64', 'utf-8')  # 选择附件
                attachment_add["Content-Type"] = 'application/octet-stream'  # 定义附件类型
                attachment_add.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=('gbk', '', file_name(i))  # 所发出的文件名默认为原文件名，这里要加入编码设置，不然中文会显示乱码
                )
                # 加入附件
                message.attach(attachment_add)

        # 连接服务器，并且发送邮件
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.host)
            smtp.login(self.user, self.password)
            smtp.sendmail(self.user, Mail.RECEIVER, message.as_string())
            print('发送成功！')
        except:
            raise Exception('发送失败，请检查密码是否正确，邮箱是否开启SMTP服务，正文格式是否正确')