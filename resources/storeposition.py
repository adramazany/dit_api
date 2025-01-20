from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.storeposition import StorePositionModel
from flask import request


class StorePosition(Resource):

    @classmethod
    def get(self, name):
        storeposition = StorePositionModel.find_by_name(name)
        if storeposition:
            return storeposition.json()
        return {"message": "StorePosition not found"}, 404

    @classmethod
    def post(self, name):
        if StorePositionModel.find_by_name(name):
            return {
                "message": "A storeposition with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        storeposition = StorePositionModel(Name=name, **data)
        try:
            storeposition.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the storeposition."}, 500

        return storeposition.json(), 201

    @classmethod
    def patch(self, name):
        storeposition = StorePositionModel.find_by_name(name)
        if not storeposition:
            return {
                "message": "A storeposition with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(storeposition, k, v)
        print(storeposition.json())

        try:
            storeposition.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the storeposition."}, 500

        return storeposition.json(), 200

    @classmethod
    def delete(self, name):
        storeposition = StorePositionModel.find_by_name(name)
        if storeposition:
            storeposition.delete_from_db()
            return {"message": "StorePosition deleted"}, 200
        return {"message": "StorePosition not found"}, 404


class StorePositionList(Resource):
    @classmethod
    def get(self):
        # return {"storepositions": [storeposition.json() for storeposition in StorePositionModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"storepositions": [storeposition.json() for storeposition in StorePositionModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
