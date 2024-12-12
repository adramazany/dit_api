from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.store import StoreModel
from flask import request


class Store(Resource):

    @classmethod
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    @classmethod
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                "message": "A store with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        store = StoreModel(Name=name, **data)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    @classmethod
    def patch(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {
                "message": "A store with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(store, k, v)
        print(store.json())

        try:
            store.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 200

    @classmethod
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        return {"message": "Store not found"}, 404


class StoreList(Resource):
    @classmethod
    def get(self):
        # return {"stores": [store.json() for store in StoreModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"stores": [store.json() for store in StoreModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
