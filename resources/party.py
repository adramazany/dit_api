from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from models.party import PartyModel
from flask import request


class Party(Resource):

    @classmethod
    def get(self, name):
        party = PartyModel.find_by_name(name)
        if party:
            return party.json()
        return {"message": "Party not found"}, 404


    @classmethod
    def patch(self, id):
        party = PartyModel.find_by_id(id)
        if not party:
            return {
                "message": "A party with id '{}' not exists.".format(id)
            }, 404

        data = request.get_json()
        for k, v in data.items():
            setattr(party, k, v)
        print(party.json())

        try:
            party.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred creating the party."}, 500

        return party.json(), 200

    @classmethod
    def delete(self, id):
        party = PartyModel.find_by_id(id)
        if party:
            party.delete_from_db()
            return {"message": "Party deleted"}, 200
        return {"message": "Party not found"}, 404


class PartyList(Resource):
    @classmethod
    def get(self):
        # return {"partys": [party.json() for party in PartyModel.find_all()]}
        data = request.args.to_dict()
        page = int(request.headers.get("page","1"))
        pageSize = int(request.headers.get("pageSize","10"))
        orderBy = request.headers.get("orderBy","")
        print(data, page, pageSize, orderBy)
        return {"partys": [party.json() for party in PartyModel.find_filter_by(page=page, pageSize=pageSize, orderBy=orderBy, **data)]}

    @classmethod
    def post(self):
        data = request.get_json()
        print(data)
        party = PartyModel(**data)
        try:
            party.save_to_db()
        except SQLAlchemyError as e:
            print(e)
            return {"message": "An error occurred creating the party."}, 500

        return party.json(), 201
