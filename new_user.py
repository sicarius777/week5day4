from flask import request

class UsersView(MethodView):
    def post(self):
        try:
            new_user_data = UserSchema().load(request.json)
            return jsonify(new_user_data), 201
        except ValidationError as err:
            return jsonify({'error': err.messages}), 400
