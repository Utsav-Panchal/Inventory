from flask_restful import Resource, reqparse
from models.usersM import UserRegisterModel


class UserRegisterResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegisterResource.parser.parse_args()

        if UserRegisterModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserRegisterModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

