"""大师相关模型"""

from plugins.private.orm import Common, db


class MasterGenre(Common, db.Model):
    """大师类型"""
    name = db.Column(db.String(length=128), nullable=False, comment='类型名')
    grade = db.Column(db.SMALLINT, nullable=False, default=0, comment='类型等级')
    superior_id = db.Column(db.Integer, db.ForeignKey('MasterGenre.id', ondelete='CASCADE'), comment='上级类型ID')


class Master(Common, db.Model):
    """大师模型"""
    name = db.Column(db.String(length=128), nullable=False, comment='大师名')
    avatar = db.Column(db.String(length=255), nullable=False, comment='大师头像')
    poster = db.Column(db.String(length=255), nullable=False, comment='大师海报')
    introduction = db.Column(db.String(length=128), default='', comment='简介')
    description = db.Column(db.Text, comment='详细描述')
    recommend = db.Column(db.SMALLINT, default=0, comment='推荐.0:不推荐,1:推荐')
    sort = db.Column(db.SMALLINT, default=0, comment='商品排序')
    genre_one = db.Column(db.Integer, db.ForeignKey('MasterGenre.id'), comment='大师分类一级')
    genre_two = db.Column(db.Integer, db.ForeignKey('MasterGenre.id'), comment='大师分类二级')
    genre_three = db.Column(db.Integer, db.ForeignKey('MasterGenre.id'), comment='大师分类三级')
