from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.user.model import Users
import json, hashlib

bp_login = Blueprint('login',__name__)
api = Api(bp_login)

class CreateTokenResource(Resource):

    # login and get token
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'args', required = True)
        parser.add_argument('password', location = 'args', required = True)

        args = parser.parse_args()

        if args['username'] == 'admin' and args['password'] == 'admin':
            token = create_access_token(identity = args['username'], user_claims = ({"id": 0, "username": "admin", "email":"admin@mail.com", "isadmin" : True}))
            return {'token' : token, 'isadmin' : True}, 200
        
        encrypted = hashlib.md5(args['password'].encode()).hexdigest()
        qry = Users.query.filter_by(username = args['username']).filter_by(password = encrypted)
        data_user = qry.first()

        if data_user is not None:
            data_user = marshal(data_user,Users.jwt_claims_fields)
            data_user['isadmin'] = False
            token = create_access_token(identity = data_user['username'], user_claims = data_user)
            return {'token' : token, 'isadmin' : False}, 200
        return{'status' : 'UNAUTHORIZED' , 'message' : 'username atau password salah'}, 401

    def options(self, id=None):
        return {'status':'ok'},200

class RefressTokenResources(Resource):

    # refresh token
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        token = create_access_token(identity = current_user)
        return {'token' : token}, 200

    def options(self, id=None):
        return {'status':'ok'},200
        
api.add_resource(CreateTokenResource,'/login')
api.add_resource(RefressTokenResources,'/refresh')