from flask import Flask, jsonify
from flask_restful import Api
#from flask_jwt_extended import JWTManager

from db import db
from resources import *

from flask_cors import CORS  # Import CORS


app = Flask(__name__)

# Configure CORS to allow all origins by default
CORS(app)
# CORS(app, origins=["http://localhost", "http://localhost:3000"])

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
api = Api(app)

with app.app_context():
    import models  # noqa: F401
    import resources  # noqa: F401

    db.create_all()


api.add_resource(Category, "/category/<string:name>")
api.add_resource(CategoryList, "/category")
api.add_resource(Part, "/part/<string:name>")
api.add_resource(PartList, "/part")
api.add_resource(Partstore, "/partstore/<int:id>")
api.add_resource(PartstoreList, "/partstore")
api.add_resource(Party, "/party/<int:id>")
api.add_resource(PartyList, "/party")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/store")
api.add_resource(StorePosition, "/storeposition/<string:name>")
api.add_resource(StorePositionList, "/storeposition")
api.add_resource(Unit, "/unit/<string:name>")
api.add_resource(UnitList, "/unit")
api.add_resource(User, "/user/<string:name>")
api.add_resource(UserList, "/user")
api.add_resource(UserLogonAudit, "/userlogonaudit/<int:id>")
api.add_resource(UserLogonAuditList, "/userlogonaudit")


if __name__ == '__main__':
     app.run()