from typing import List, Dict, Any

try:
    from model import db
except (ImportError, ModuleNotFoundError):
    from pysubway.model import db


class Company(db.Model):
    __tablename__ = 'company'
    __bind_key__ = 'guard'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False, unique=True)
    name = db.Column(db.String(32, u'utf8_bin'), nullable=False)
    encryption_type = db.Column(db.Integer, nullable=False)
    company_pub_secret_key = db.Column(db.String(1024), nullable=False)
    producer_prv_secret_key = db.Column(db.String(2048), nullable=False)
    aes_key = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(20, u'utf8_bin'), nullable=False)
    contact_mobile = db.Column(db.String(13), nullable=False)
    contact_email = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.Integer, nullable=True)
    remark = db.Column(db.String(200, u'utf8_bin'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)

    @classmethod
    def get_one(cls, **fields: Dict[str, Any]) -> 'Company':
        return cls.query.filter_by(**fields).first()

    @classmethod
    def get_all(cls) -> List['Company']:
        return cls.query.all()


