try:
    from model import db
except (ImportError, ModuleNotFoundError):
    from pysubway.model import db


class CompanyRechargeJournal(db.Model):
    __tablename__ = "company_recharge_journal"
    __bind_key__ = 'guard'

    id = db.Column(db.Integer, primary_key=True)
    company_uuid = db.Column(db.String(128), nullable=False, comment="")
    recharge_order_sn = db.Column(db.String(128), nullable=True, comment="")
    real_money = db.Column(db.Integer, nullable=True, comment='')
    net_money = db.Column(db.Integer, nullable=True, comment="")
    pay_at = db.Column(db.DateTime, nullable=True, comment="")
    status = db.Column(db.Integer, nullable=True, comment="")
    pay_type = db.Column(db.String(64), nullable=True, comment="")
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)
