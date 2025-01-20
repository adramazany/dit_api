from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.part import PartModel
from flask import request


class Part(Resource):

    @classmethod
    def get(self, name):
        part = PartModel.find_by_name(name)
        if part:
            return part.json()
        return {"message": "Part not found"}, 404

    @classmethod
    def post(self, name):
        if PartModel.find_by_name(name):
            return {
                "message": "A part with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        part = PartModel(Name=name, **data)
        try:
            part.save_to_db()
        except SQLAlchemyError as e:
            print(e)
            return {"message": "An error occurred creating the part."}, 500
        except exception as e:
            print(e)
            return {"message": e.message}, 500

        return part.json(), 201

    @classmethod
    def patch(self, name):
        part = PartModel.find_by_name(name)
        if not part:
            return {
                "message": "A part with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(part, k, v)
        print(part.json())

        try:
            part.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the part."}, 500

        return part.json(), 200

    @classmethod
    def delete(self, name):
        part = PartModel.find_by_name(name)
        if part:
            part.delete_from_db()
            return {"message": "Part deleted"}, 200
        return {"message": "Part not found"}, 404


class PartList(Resource):
    @classmethod
    def get(self):
        # return {"parts": [part.json() for part in PartModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"parts": [part.json() for part in PartModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
