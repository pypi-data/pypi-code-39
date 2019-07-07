# 主模型层
from plugins.private.orm import Common, db, PasswordModel


class Admin(Common, db.Model, PasswordModel):
    """管理员模型"""

    name = db.Column(db.String(50), default='', comment='管理员名字')
    nickname = db.Column(db.String(50), default='', comment='管理员昵称')
    role = db.Column(db.String(50), default='', comment='管理员角色')
    type = db.Column(db.Enum('xxx', 'ccc'), nullable=False, comment='管理员类型')
    _password = db.Column('password', db.String(128), nullable=False, comment='账号密码')


class Roles(Common, db.Model):
    """管理员角色模型"""

    name = db.Column(db.String(50), default='', comment='角色名称')
    role_content = db.Column(db.String(50), default='', comment='角色内容')


