# 主模型层
from plugins.private.orm import Common, db, PasswordModel


class Admin(Common, db.Model, PasswordModel):
    """管理员模型"""

    name = db.Column(db.String(50), default='', comment='管理员名字/昵称')
    account = db.Column(db.String(50), nullable=False, comment='登录账号')
    _password = db.Column('password', db.String(128), nullable=False, comment='账号密码')


class Source(Common, db.Model):
    """资源管理"""

    _privacy_fields = {'status', 'ip_address'}

    genre = db.Column(db.Enum('oss', 'local', 'oss_user'), nullable=False, comment='资源类型,oss或本地资源')
    file_genre = db.Column(db.Enum('image', 'video', 'code', 'other', 'folder'), nullable=False, comment='资源类型,文件类型')
    file_name = db.Column(db.String(255), nullable=False, comment='资源文件名')
    folder = db.Column(db.String(255), default='', index=True, comment='文件夹名')
    ip_address = db.Column(db.String(255), comment='资源文件上传ip')
    size = db.Column(db.Integer, nullable=False, default=0, comment='文件大小')
    description = db.Column(db.String(255), default='', comment='资源描述')
    user_id = db.Column(db.Integer, default=0, comment='用户编号')
