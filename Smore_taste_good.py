from flask import Flask, jsonify, request
from flask.views import MethodView
from flask_smorest import Api, Blueprint
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)
api = Api(app)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True)

class ShipSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    model = fields.String(required=True)

users_bp = Blueprint('users', __name__, url_prefix='/users')
ships_bp = Blueprint('ships', __name__, url_prefix='/ships')

class UsersView(MethodView):
    def get(self):
        pass

    def post(self):
        pass

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass

class ShipsView(MethodView):
    def get(self):
        pass

    def post(self):
        pass

    def put(self, ship_id):
        pass

    def delete(self, ship_id):
        pass


users_bp.add_url_rule('', view_func=UsersView.as_view('users'))
ships_bp.add_url_rule('', view_func=ShipsView.as_view('ships'))


api.register_blueprint(users_bp)
api.register_blueprint(ships_bp)

if __name__ == '__main__':
    app.run(debug=True)
