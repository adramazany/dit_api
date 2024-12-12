from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.category import CategoryModel
from flask import request


class Category(Resource):

    @classmethod
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {"message": "Category not found"}, 404

    @classmethod
    def post(self, name):
        if CategoryModel.find_by_name(name):
            return {
                "message": "A category with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        category = CategoryModel(Name=name, **data)
        try:
            category.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 201

    @classmethod
    def patch(self, name):
        category = CategoryModel.find_by_name(name)
        if not category:
            return {
                "message": "A category with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(category, k, v)
        print(category.json())

        try:
            category.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the category."}, 500

        return category.json(), 200

    @classmethod
    def delete(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()
            return {"message": "Category deleted"}, 200
        return {"message": "Category not found"}, 404


class CategoryList(Resource):
    @classmethod
    def get(self):
        # return {"categories": [category.json() for category in CategoryModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"categories": [category.json() for category in CategoryModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
