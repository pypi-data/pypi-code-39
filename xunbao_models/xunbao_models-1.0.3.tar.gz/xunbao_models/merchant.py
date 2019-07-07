"""商家模型相关"""
from plugins.private.orm import Common, db, PasswordModel, SortMode


class Merchant(Common, db.Model, SortMode, PasswordModel):
    """商家
    关闭商家:status字段标识此状态
    """
    name = db.Column(db.String(length=12), comment='商家名称')
    logo = db.Column(db.String(length=255), default='', comment='商标')
    merchant_type = db.Column(db.Integer, comment='商家分类.1:优店,2:古玩,3:画廊')
    phone = db.Column(db.String(11), nullable=False, comment='电话号码')
    _password = db.Column('password', db.String(length=255), nullable=False, comment='登录密码')
    genre = db.Column(db.SMALLINT, nullable=False, comment='店铺类型.0:个人商家,1:企业商家')
    payment_type = db.Column(db.SMALLINT, default=0, comment='缴费类型,0:保证金,1:入住费')
    money = db.Column(db.Integer, default=0, comment='缴费金额')
    score = db.Column(db.SMALLINT, default=10, comment='店铺评分')
    collection = db.Column(db.Integer, default=0, comment='关注/收藏.计数')
    do_business = db.Column(db.SMALLINT, default=0, comment='营业状态. 0:未营业, 1:营业中')
    description = db.Column(db.String(255), default='', comment='店铺描述')
    old_id = db.Column(db.String(255))
    release = db.Column(db.SMALLINT, default=1, comment='是否显示. 0:不显示, 1:显示')

    _privacy_fields = {'password'}


class MerchantApplication(Common, db.Model):
    """商家入驻申请"""

    # 商家基础信息
    merchant_name = db.Column(db.String(length=12), unique=True, comment='商家名称')
    logo = db.Column(db.String(length=255), default='', comment='商标')
    merchant_type = db.Column(db.Integer, comment='商家分类')
    phone = db.Column(db.String(11), nullable=False, comment='电话号码')
    payment_type = db.Column(db.SMALLINT, default=0, comment='缴费类型,0:保证金,1:入住费')
    money = db.Column(db.Integer, default=0, comment='缴费金额')
    description = db.Column(db.String(255), default='', comment='店铺描述')
    genre = db.Column(db.SMALLINT, nullable=False, comment='店铺类型.0:个人商家,1:企业商家')

    name = db.Column(db.String(length=30), nullable=False, comment='申请人姓名')
    id_card = db.Column(db.String(length=18), nullable=False, comment='申请人身份证号')
    id_card_facade = db.Column(db.String(length=255), nullable=False, comment='申请人身份证照片,正面')
    id_card_back = db.Column(db.String(length=255), nullable=False, comment='申请人身份证照片,背面')
    id_card_handheld = db.Column(db.String(length=255), nullable=False, comment='申请人身份证照片,手持照')

    enterprise_name = db.Column(db.String(length=100), unique=True, comment='企业名')
    business_license = db.Column(db.String(100), unique=True, comment='营业执照副本照片')
    legal_person = db.Column(db.String(100), comment='法人名字')
    legal_person_id_card = db.Column(db.String(18), comment='法人身份证号')
    legal_person_id_card_facade = db.Column(db.String(255), comment='法人身份证正面')
    legal_person_id_card_back = db.Column(db.String(255), comment='法人身份证反面')

    application_status = db.Column(db.SMALLINT, default=-1, comment='审核状态.-1:未审核,0:审核失败,1:审核通过')
