# 用户型层
from werkzeug.security import generate_password_hash, check_password_hash
from plugins.private.orm import Common, db, PasswordModel


class User(Common, db.Model, PasswordModel):
    """用户表"""

    _privacy_fields = {'status', '_password', '_pay_password', 'token'}

    uuid = db.Column(db.String(length=32), nullable=False, unique=True, index=True, comment='用户唯一识别码')
    account = db.Column(db.String(length=16), default='', comment='账户')
    phone = db.Column(db.String(length=16), nullable=False, index=True, comment='手机')
    _nickname = db.Column('nickname', db.String(length=16), default='有梦想的名字', index=True, comment='用户昵称')
    _password = db.Column('password', db.String(length=255), nullable=False, comment='用户密码:加密内容')
    avatar = db.Column(db.String(length=255), default='', comment='用户头像')
    gender = db.Column(db.SMALLINT, default=0, comment='用户性别.0:保密,1:男,2:女')
    money = db.Column(db.DECIMAL(9, 2), default=0.0, comment='余额')
    _pay_password = db.Column('pay_password', db.String(length=255), nullable=False, comment='用户密码:加密内容')
    token = db.Column(db.String(length=32), default='', comment='某种凭证,目前未知')
    self_media = db.Column(db.SMALLINT, default=0, comment='是否属于自媒体,0:否, 1:是')

    @property
    def pay_password(self):
        return self._pay_password

    @pay_password.setter
    def pay_password(self, raw: str) -> None:
        """原始交易密码加密
        :param raw: 用户输入的始交易密码
        """
        self._pay_password = generate_password_hash(raw)

    def check_pay_password(self, raw: str) -> bool:
        """检验用户输入的始交易密码
        :param raw: 用户输入的始交易密码
        """
        return check_password_hash(self._pay_password, raw)

    @property
    def nickname(self):
        """昵称"""
        return self._nickname

    @nickname.setter
    def nickname(self, value: str):
        """设置昵称"""
        if value:
            self._nickname = value
        else:
            self._nickname = f'{self.phone[:4]}xbw{self.phone[7:]}'


class UserAddress(Common, db.Model):
    """用户地址"""

    user_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='CASCADE'), comment='用户编号')
    phone = db.Column(db.String(length=16), nullable=False, index=True, comment='手机')
    province = db.Column(db.String(length=30), nullable=False, index=True, comment='省')
    city = db.Column(db.String(length=30), nullable=False, comment='市')
    area = db.Column(db.String(length=30), nullable=False, comment='区')
    address = db.Column(db.String(length=255), nullable=False, comment='详细地址')
    default = db.Column(db.SMALLINT, default=0, comment='默认地址.0:不是, 1:是')
    tag = db.Column(db.String(length=10), default='', comment='地址标签')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'default', name='uix_user_id_default'),
        db.Index('ix_user_id_default', 'user_id', 'default'),
    )
