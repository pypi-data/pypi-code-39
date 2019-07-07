from plugins.private.orm import Common, db


class Area(Common, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    code = db.Column(db.Integer, comment='地区编码')
    name = db.Column(db.String(32), comment='地区名称')
    level = db.Column(db.SMALLINT, comment='地区级别，1为省，2为市，3为区/县')
    parent_code = db.Column(db.Integer, comment='上级地区code编码')
    create_time = None
    status = None
