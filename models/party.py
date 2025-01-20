from datetime import datetime

from sqlalchemy import text

from db import db


class PartyModel(db.Model):
    __tablename__ = "GNR.Party"
    # __table_args__ = {"schema": "GNR"}

    PartyID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(50), nullable=True)
    FirstName = db.Column(db.String(50), nullable=True)
    LastName = db.Column(db.String(50), nullable=True)
    Alias = db.Column(db.String(50), nullable=True)
    NationalID = db.Column(db.String(20), nullable=True)
    Gender = db.Column(db.Integer, nullable=True)
    Nationality = db.Column(db.String(20), nullable=True)
    Mobile = db.Column(db.String(20), nullable=True)
    Email = db.Column(db.String(50), nullable=True)
    #BirthDate = db.Column(db.DateTime, nullable=True)
    BirthDate = db.Column(db.String(100), nullable=True)
    EducationDegree = db.Column(db.Integer, nullable=True)
    #MarriageDate = db.Column(db.DateTime, nullable=True)
    MarriageDate = db.Column(db.String(100), nullable=True)
    Creator = db.Column(db.String(100), nullable=False, default='Admin')
    #CreationDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    CreationDate = db.Column(db.String(100), nullable=False, default=datetime.utcnow())
    LastModifier = db.Column(db.String(100), nullable=False, default='Admin')
    #LastModificationDate = db.Column(db.DateTime, nullable=False, onupdate=datetime.utcnow())
    LastModificationDate = db.Column(db.String(100), nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def json(self):
        return {
            "PartyID": self.PartyID,
            "Title":   self.Title,
            "FirstName":   self.FirstName,
            "LastName":    self.LastName,
            "Alias":   self.Alias,
            "NationalID":  self.NationalID,
            "Gender":  self.Gender,
            "Nationality": self.Nationality,
            "Mobile":  self.Mobile,
            "Email":   self.Email,
            "BirthDate":   self.BirthDate,
            "EducationDegree": self.EducationDegree,
            "MarriageDate":    self.MarriageDate,
            "Creator": self.Creator,
            "CreationDate":    self.CreationDate,
            "LastModifier":    self.LastModifier,
            "LastModificationDate":    self.LastModificationDate,
        }

    @classmethod
    def find_by_id(self, PartyID):
        return self.query.filter_by(PartyID=PartyID).first()

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
