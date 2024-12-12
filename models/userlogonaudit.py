from sqlalchemy import text

from db import db


class UserLogonAuditModel(db.Model):
    __tablename__ = "SYS1.UserLogonAudit"
    # __table_args__ = {"schema": "GNR"}

    UserLogonAuditID = db.Column(db.Integer, primary_key=True)
    UserRef = db.Column(db.Integer, nullable=False)
    LogonTime = db.Column(db.DateTime, nullable=False)
    LogonSource = db.Column(db.String(100), nullable=True)
    SessionID = db.Column(db.String(50), nullable=False)
    LogoutReason = db.Column(db.String(200), nullable=True)
    LogoutTime = db.Column(db.DateTime, nullable=True)
    LastActivityTime = db.Column(db.DateTime, nullable=False)
    Version = db.Column(db.DateTime, nullable=False)

    def json(self):
        return {
            "UserLogonAuditID": self.UserLogonAuditID,
            "UserRef": self.UserRef,
            "LogonTime": self.LogonTime,
            "LogonSource": self.LogonSource,
            "SessionID": self.SessionID,
            "LogoutReason": self.LogoutReason,
            "LogoutTime": self.LogoutTime,
            "LastActivityTime": self.LastActivityTime,
            "Version": self.Version,
        }

    @classmethod
    def find_by_id(self, id):
        return self.query.filter_by(UserLogonAuditID=id).all()

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
