from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_simple import create_jwt, jwt_required

from models.user import UserModel


class UserRegister(Resource):
    allowed_args = {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
    }

    @use_args(allowed_args)
    def post(self, args):
        if UserModel.find_by_username(args['username']):
            return {'message': 'user already exists'}
        user = UserModel(**args)
        user.save_to_db()
        return {'message': 'user created'}, 201


class UserLogin(Resource):
    allowed_args = {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
    }

    @use_args(allowed_args)
    def post(self, args):
        user = UserModel.find_by_username(args['username'])
        if user and user.password == args['password']:
            return {'jwt': create_jwt(identity=user.username)}
        return {'message': 'access denied'}


class UserList(Resource):
    @jwt_required
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
