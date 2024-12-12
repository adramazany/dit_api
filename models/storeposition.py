from enum import unique

from sqlalchemy import text

from db import db


class StorePositionModel(db.Model):
    __tablename__ = "LGS.StorePosition"
    # __table_args__ = {"schema": "GNR"}

    StorePositionID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=False)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    State = db.Column(db.Integer, nullable=False)
    StoreRef = db.Column(db.Integer, nullable=False)
    ParentRef = db.Column(db.Integer, nullable=True)

    def json(self):
        return {
            "StorePositionID": self.StorePositionID,
            "Code": self.Code,
            "Name": self.Name,
            "State": self.State,
            "StoreRef": self.StoreRef,
            "ParentRef": self.ParentRef,
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
