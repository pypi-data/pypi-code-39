# 消息型层
from plugins.private.orm import Common, db


class SystemMessage(Common, db.Model):
    """系统消息"""

    title = db.Column(db.String(length=255), nullable=False, comment='标题')
    introduction = db.Column(db.String(length=255), default='', comment='简介')
    cover = db.Column(db.String(length=255), default='', comment='封面图')
    content = db.Column(db.String(length=1000), comment='内容')
    parameter = db.Column(db.JSON, comment='参数')


class SystemMessageLog(Common, db.Model):
    """系统消息已读日志"""

    message_id = db.Column(db.Integer, db.ForeignKey(SystemMessage.id, ondelete='CASCADE'), comment='系统消息ID')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), comment='用户ID')
    view = db.Column(db.SMALLINT, default=0, comment='消息查看状态.0:未查看,1:已查看')
