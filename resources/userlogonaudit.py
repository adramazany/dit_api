from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.userlogonaudit import UserLogonAuditModel
from flask import request


class UserLogonAudit(Resource):

    @classmethod
    def get(self, name):
        userlogonaudit = UserLogonAuditModel.find_by_name(name)
        if userlogonaudit:
            return userlogonaudit.json()
        return {"message": "UserLogonAudit not found"}, 404

    @classmethod
    def patch(self, id):
        userlogonaudit = UserLogonAuditModel.find_by_id(id)
        if not userlogonaudit:
            return {
                "message": "A userlogonaudit with id '{}' not exists.".format(id)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(userlogonaudit, k, v)
        print(userlogonaudit.json())

        try:
            userlogonaudit.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the userlogonaudit."}, 500

        return userlogonaudit.json(), 200

    @classmethod
    def delete(self, id):
        userlogonaudit = UserLogonAuditModel.find_by_id(id)
        if userlogonaudit:
            userlogonaudit.delete_from_db()
            return {"message": "UserLogonAudit deleted"}, 200
        return {"message": "UserLogonAudit not found"}, 404


class UserLogonAuditList(Resource):
    @classmethod
    def get(self):
        # return {"userlogonaudits": [userlogonaudit.json() for userlogonaudit in UserLogonAuditModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"userlogonaudits": [userlogonaudit.json() for userlogonaudit in UserLogonAuditModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}

    @classmethod
    def post(self):
        data = request.get_json()
        print(data)
        userlogonaudit = UserLogonAuditModel(**data)
        try:
            userlogonaudit.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the userlogonaudit."}, 500

        return userlogonaudit.json(), 201
