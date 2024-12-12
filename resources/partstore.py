from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.partstore import PartstoreModel
from flask import request


class Partstore(Resource):

    @classmethod
    def get(self, id):
        partstore = PartstoreModel.find_by_id(id)
        if partstore:
            return partstore.json()
        return {"message": "Partstore not found"}, 404

    @classmethod
    def patch(self, id):
        partstore = PartstoreModel.find_by_id(id)
        if not partstore:
            return {
                "message": "A partstore with id '{}' not exists.".format(id)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(partstore, k, v)
        print(partstore.json())

        try:
            partstore.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred updating the partstore."}, 500

        return partstore.json(), 200

    @classmethod
    def delete(self, id):
        partstore = PartstoreModel.find_by_id(id)
        if partstore:
            partstore.delete_from_db()
            return {"message": "Partstore deleted"}, 200
        return {"message": "Partstore not found"}, 404


class PartstoreList(Resource):
    @classmethod
    def get(self):
        # return {"partstores": [part.json() for part in PartstoreModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"partstores": [part.json() for part in PartstoreModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}

    @classmethod
    def post(self):
        data = request.get_json()
        print(data)
        partstore = PartstoreModel(**data)
        try:
            partstore.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the partstore."}, 500

        return partstore.json(), 201

