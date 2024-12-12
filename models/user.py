from datetime import datetime

from sqlalchemy import text

from db import db


class UserModel(db.Model):
    __tablename__ = "SYS1.User"
    # __table_args__ = {"schema": "GNR"}

    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    PartyRef = db.Column(db.Integer, nullable=True)
    IsAdministrator = db.Column(db.Boolean, nullable=True)
    Password = db.Column(db.String(50), nullable=True)
    LastPasswordUpdate = db.Column(db.DateTime, nullable=False)
    Creator = db.Column(db.Integer, nullable=False)
    CreationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    LastModifier = db.Column(db.Integer, nullable=False)
    LastModificationDate = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow())

    def json(self):
        return {
            "UserID": self.UserID,
            "Name": self.Name,
            "Status": self.Status,
            "PartyRef": self.PartyRef,
            "IsAdministrator": self.IsAdministrator,
            "Password": "***",
            "LastPasswordUpdate": self.LastPasswordUpdate,
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
