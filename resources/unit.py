from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.unit import UnitModel
from flask import request


class Unit(Resource):

    @classmethod
    def get(self, name):
        unit = UnitModel.find_by_name(name)
        if unit:
            return unit.json()
        return {"message": "Unit not found"}, 404

    @classmethod
    def post(self, name):
        if UnitModel.find_by_name(name):
            return {
                "message": "A unit with name '{}' already exists.".format(name)
            }, 400

        #data = self.parser.parse_args()
        data = request.get_json()
        print(data)
        unit = UnitModel(Name=name, **data)
        try:
            unit.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the unit."}, 500

        return unit.json(), 201

    @classmethod
    def patch(self, name):
        unit = UnitModel.find_by_name(name)
        if not unit:
            return {
                "message": "A unit with name '{}' not exists.".format(name)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(unit, k, v)
        print(unit.json())

        try:
            unit.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the unit."}, 500

        return unit.json(), 200

    @classmethod
    def delete(self, name):
        unit = UnitModel.find_by_name(name)
        if unit:
            unit.delete_from_db()
            return {"message": "Unit deleted"}, 200
        return {"message": "Unit not found"}, 404


class UnitList(Resource):
    @classmethod
    def get(self):
        # return {"units": [unit.json() for unit in UnitModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"units": [unit.json() for unit in UnitModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}
