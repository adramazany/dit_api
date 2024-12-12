from sqlalchemy import text

from db import db


class UnitModel(db.Model):
    __tablename__ = "GNR.Unit"
    # __table_args__ = {"schema": "GNR"}

    UnitID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    AbbreviatedName = db.Column(db.String(256), nullable=True)
    #items = db.relationship("ItemModel", back_populates="unit", lazy="dynamic")

    def json(self):
        return {
            "UnitID": self.UnitID,
            "Name": self.Name,
            "AbbreviatedName": self.AbbreviatedName,
            # "items": [item.json() for item in self.items.all()],
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
