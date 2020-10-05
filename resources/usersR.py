from flask_restful import Resource, reqparse
from models.usersM import UserRegisterModel


class UserRegisterResource(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('username',
                       required=True,
                       help='Username field can not be blank.')
    parse.add_argument('password',
                       required=True,
                       help='password field can not be blank.')

    def post(self):
        data = UserRegisterResource.parse.parse_args()
        user = UserRegisterModel(**data)
        user_check = user.find_by_name()
        if user_check is None:
            user.save_to_db()
        else:
            return {"message": f"{data['username']} is already exists."}, 201
        return {"message": f"user -> {data['username']} is added."}, 201

