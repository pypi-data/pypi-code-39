from typing import Tuple

try:
    from model import db
except (ImportError, ModuleNotFoundError):
    from pysubway.model import db


class CompanyProduct(db.Model):
    __tablename__ = 'company_product'
    __bind_key__ = 'guard'

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.ForeignKey(u'product.service_name'), nullable=False, index=True)
    mode = db.Column(db.String(128), nullable=False)
    company_uuid = db.Column(db.ForeignKey(u'company.uuid'), nullable=False, index=True)
    type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer)
    limit_day = db.Column(db.Integer, nullable=False)
    limit_total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.ForeignKey(u'user.id'), nullable=False, index=True)
    price = db.Column(db.Integer, nullable=True)
    create_at = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_at = db.Column(db.DateTime)
    delete_at = db.Column(db.DateTime)

    @classmethod
    def get_product_by_uuid(cls, company_uuid: str) -> Tuple:
        return cls.query(cls.service_name, cls.mode).filter_by(company_uuid=company_uuid).all()

    @classmethod
    def has_permission_for_product(cls, company_uuid: str, service: str, mode: str) -> bool:
        return cls.query.filter_by(service_name=service, mode=mode, company_uuid=company_uuid).first() is not None
