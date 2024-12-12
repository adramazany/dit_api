from sqlalchemy import text

from db import db


class StoreModel(db.Model):
    __tablename__ = "LGS.Store"
    # __table_args__ = {"schema": "GNR"}

    StoreID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128), nullable=False)
    Code = db.Column(db.String(64), nullable=False)
    State = db.Column(db.Integer, nullable=False)

    def json(self):
        return {
            "StoreID": self.StoreID,
            "Name": self.Name,
            "Code": self.Code,
            "State": self.State,
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
