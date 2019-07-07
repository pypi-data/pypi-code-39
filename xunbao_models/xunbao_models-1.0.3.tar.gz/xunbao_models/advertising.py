"""广告模型"""
from plugins.private.orm import Common, db


class CarouselColumn(Common, db.Model):
    """轮播图版块
    一级分类:首页板块
    二级分类:子版块
    """
    __tablename__ = 'carousel_column'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自动编号')
    name = db.Column(db.String(length=10), nullable=False, comment='栏目名/板块名')
    icon = db.Column(db.String(length=255), default='', comment='栏目图标')
    grade = db.Column(db.SMALLINT, nullable=False, comment='类型等级.1:一级,2:二级')
    superior_id = db.Column(db.Integer, db.ForeignKey('carousel_column.id', ondelete='CASCADE'), comment='上级类型')

    carousel = db.relationship("Carousel", backref="carousel_column")

    superior = db.relationship('CarouselColumn', lazy='select', backref=db.backref('subordinate', cascade='all,delete'),
                               remote_side=id)

    __table_args__ = (
        db.UniqueConstraint('name', 'superior_id', name='uix_name_superior'),
        db.Index('ix_name_superior_type', 'name', 'superior_id'),
    )

    def subordinates(self):
        """获取所有子集"""
        superior = {**self._serialization(), 'children': []}

        for subordinate in self.subordinate:
            superior['children'].append(subordinate.subordinates())
        return superior

    def _serialization(self):
        """自定义序列化
        """
        carousel_num = Carousel.query.filter_by(column_id=self.id).count()
        result = self.serialization()
        result.update({'carousel_num': carousel_num})
        return result


class Carousel(Common, db.Model):
    """轮播图"""

    name = db.Column(db.String(length=16), default='', comment='轮播图名字')
    interval = db.Column(db.SMALLINT, comment='平均间隔')
    images = db.Column(db.JSON, comment='轮播图图片')
    description = db.Column(db.String(length=255), default='', comment='描述')
    release = db.Column(db.SMALLINT, default=1, comment='是否显示')
    sort = db.Column(db.SMALLINT, default=0, comment='排序')

    column_id = db.Column(db.Integer, db.ForeignKey('carousel_column.id', ondelete='CASCADE'), comment='轮播图版块id')