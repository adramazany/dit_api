from sqlalchemy import text

from db import db


class CategoryModel(db.Model):
    __tablename__ = "LGS.Category"
    # __table_args__ = {"schema": "GNR"}

    CategoryID = db.Column(db.Integer, primary_key=True)
    Code = db.Column(db.String(64), unique=True, nullable=False)
    Name = db.Column(db.String(256), unique=True, nullable=False)
    PricingMethod = db.Column(db.String(256), nullable=True)

    def json(self):
        return {
            "CategoryID": self.CategoryID,
            "Code": self.Code,
            "Name": self.Name,
            "PricingMethod": self.PricingMethod,
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
