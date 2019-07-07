"""商品相关模型"""

from plugins.private.orm import Common, db, SortMode


class CommodityGenre(Common, db.Model):
    """商品类型"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='自动编号')
    name = db.Column(db.String(length=16), nullable=False, comment='商品名')
    icon = db.Column(db.String(length=255), nullable='', comment='类型图标')
    grade = db.Column(db.SMALLINT, nullable=False, comment='类型等级.1:一级,2:二级')
    superior_id = db.Column(db.Integer, db.ForeignKey('commodity_genre.id', ondelete='CASCADE'), comment='类型上级类型')
    stage_name = db.Column(db.String(length=8), comment='')

    superior = db.relationship('CommodityGenre', lazy='select', backref=db.backref('subordinate', cascade='all,delete'),
                               remote_side=id)

    __table_args__ = (
        db.UniqueConstraint('name', 'superior_id', name='uix_name_superior'),
        db.Index('ix_name_superior_type', 'name', 'superior_id'),
    )

    def subordinates(self):
        """获取所有子集"""
        superior = {**self.serialization(), 'children': []}

        for subordinate in self.subordinate:
            superior['children'].append(subordinate.subordinates())
        return superior

    def children_info(self, result: dict, *args, **kwargs):
        """占位方法"""
        result.update({'children': list()})


class CommodityTag(Common, db.Model):
    """商品标签"""

    name = db.Column(db.String(length=10), nullable=False, unique=True, comment='标签名')
    description = db.Column(db.String(length=100), default='', comment='标签描述')


class CommodityTagsRelation(Common, db.Model):
    """商品标签关系"""

    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id', ondelete='CASCADE'), nullable=False,
                             comment='商品id')
    tag_id = db.Column(db.Integer, db.ForeignKey('commodity_tag.id', ondelete='CASCADE'), nullable=False,
                       comment='标签id')

    tag = db.relationship('CommodityTag', foreign_keys=[tag_id])


class Commodity(Common, db.Model):
    """商品"""

    name = db.Column(db.String(length=64), nullable=False, comment='商品名')
    code = db.Column(db.String(length=40), nullable=False, unique=True, comment='商品唯一码')
    subtitle = db.Column(db.String(length=64), default='', comment='副标题')
    author = db.Column(db.String(length=20), default='', comment='作者')
    years = db.Column(db.Integer, default=0, comment='公元年份.0:未知年份,years>0:公元后,years<0:公元前')
    price = db.Column(db.DECIMAL(11, 2), default=0.00, comment='商品价格')
    images = db.Column(db.JSON, default=list, comment='图片')
    thumbnail = db.Column(db.String(length=255), default='', comment='缩略图')
    sort = db.Column(db.SMALLINT, default=0, comment='店铺排序')
    top = db.Column(db.SMALLINT, default=0, comment='店铺置顶')
    release = db.Column(db.SMALLINT, default=1, comment='店铺显示')
    recommend = db.Column(db.SMALLINT, default=0, comment='店铺推荐')
    boutique = db.Column(db.SMALLINT, default=0, comment='店铺精品')
    description = db.Column(db.Text, comment='详情/介绍')
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id', ondelete='CASCADE'), comment='商家ID')
    genre_one = db.Column(db.Integer, db.ForeignKey('commodity_genre.id'), comment='一级分类')
    genre_two = db.Column(db.Integer, db.ForeignKey('commodity_genre.id'), comment='二级分类')
    application_status = db.Column(db.SMALLINT, default=-1, comment='审核状态.-1:未审核,0:审核失败,1:审核通过')

    merchant = db.relationship('Merchant')

    def merchant_info(self, result: dict, *args, **kwargs):
        """商家详情"""

        result.update({'merchant_info': self.merchant.serialization()})


class CommodityReview(Common, db.Model):
    """商品审核表"""

    commodity_id = db.Column(db.Integer, db.ForeignKey('commodity.id'), nullable=False, comment='商品id')
    snapshot = db.Column(db.JSON, default=dict, comment='申请时商品详情')
    genre = db.Column(db.SMALLINT, default=1, comment='申请类型.1:系统自动申请, 2:用户主动申请')
    operating_genre = db.Column(db.SMALLINT, default=1, comment='操作类型.1:添加, 2:编辑')
    message = db.Column(db.String(length=128), default='', comment='申请留言')
    reply = db.Column(db.String(length=255), default='', comment='申请审核回复')
    application_status = db.Column(db.SMALLINT, default=-1, comment='审核状态.-1:未审核,0:审核失败,1:审核通过')

    commodity = db.relationship('Commodity')

    def merchant_info(self, result: dict, *args, **kwargs):
        """补充商家详情"""

        result.update({'merchant_info': self.commodity.merchant.serialization()})

    # 修改替换快照中的商品类型，原id返回类型名称
    def re_edit_snapshot(self, result: dict, *args, **kwargs):
        genre_two = self.snapshot['genre_two']
        commodity_genre = CommodityGenre.query.filter_by(id=genre_two).first()
        if commodity_genre:
            self.snapshot['genre_one'] = commodity_genre.superior.name
            self.snapshot['genre_two'] = commodity_genre.name
