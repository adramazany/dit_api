from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel
from flask import request


class User(Resource):

    @classmethod
    def get(self, name):
        user = UserModel.find_by_name(name)
        if user:
            return user.json()
        return {"message": "User not found"}, 404

    @classmethod
    def post(self, name):
        if UserModel.find_by_name(name):
            return {
                "message": "A user with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        user = UserModel(Name=name, **data)
        try:
            user.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the user."}, 500

        return user.json(), 201

    @classmethod
    def patch(self, name):
        user = UserModel.find_by_name(name)
        if not user:
            return {
                "message": "A user with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(user, k, v)
        print(user.json())

        try:
            user.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the user."}, 500

        return user.json(), 200

    @classmethod
    def delete(self, name):
        user = UserModel.find_by_name(name)
        if user:
            user.delete_from_db()
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404


class UserList(Resource):
    @classmethod
    def get(self):
        # return {"users": [user.json() for user in UserModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"users": [user.json() for user in UserModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
