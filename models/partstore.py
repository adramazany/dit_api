from sqlalchemy import text

from db import db


class PartstoreModel(db.Model):
    __tablename__ = "LGS.Partstore"
    # __table_args__ = {"schema": "GNR"}

    PartstoreID = db.Column(db.Integer, primary_key=True)
    PartRef = db.Column(db.Integer, nullable=False)
    StoreRef = db.Column(db.Integer, nullable=False)
    PositionRef = db.Column(db.Integer, nullable=True)
    State = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "PartstoreID": self.PartstoreID,
            "PartRef": self.PartRef,
            "StoreRef": self.StoreRef,
            "PositionRef": self.PositionRef,
            "State": self.State,
        }

    @classmethod
    def find_by_id(self, PartstoreID):
        return self.query.filter_by(PartstoreID=PartstoreID).first()

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

