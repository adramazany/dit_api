from datetime import datetime

from sqlalchemy import text

from db import db


class PartModel(db.Model):
    __tablename__ = "LGS.Part"
    # __table_args__ = {"schema": "GNR"}

    PartID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=False)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    MajorUnitRef = db.Column(db.Integer, nullable=False)
    CategoryRef = db.Column(db.Integer, nullable=True)
    QRCode = db.Column(db.String(256), nullable=True)
    Quantity = db.Column(db.Integer, nullable=True)
    Creator = db.Column(db.Integer, nullable=False, default='Admin')
    #CreationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()) # TypeError: Object of type datetime is not JSON serializable
    CreationDate = db.Column(db.String(100), nullable=False, default=datetime.utcnow())
    LastModifier = db.Column(db.String(100), nullable=False, default='Admin')
    #LastModificationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())
    LastModificationDate = db.Column(db.String(100), nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def json(self):
        return {
            "PartID": self.PartID,
            "Code": self.Code,
            "Name": self.Name,
            "MajorUnitRef": self.MajorUnitRef,
            "CategoryRef": self.CategoryRef,
            "QRCode": self.QRCode,
            "Quantity": self.Quantity,
            "Creator": self.Creator,
            "CreationDate": self.CreationDate,
            "LastModifier": self.LastModifier,
            "LastModificationDate": self.LastModificationDate,
        }

    @classmethod
    def find_by_name(self, name):
        return self.query.filter_by(Name=name).first()

    @classmethod
    def find_all(self):
        return self.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_filter_by(self, page=1, pageSize=10, orderBy="", **kwargs):
        return self.query.filter_by(**kwargs).order_by(text(orderBy)).paginate(page=page, per_page=pageSize)
