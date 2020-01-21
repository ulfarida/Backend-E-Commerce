from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.user.model import Users
import json, hashlib
from password_strength import PasswordPolicy
from blueprints import db, app

bp_password = Blueprint('password',__name__)
api = Api(bp_password)

class PasswordResources(Resource):
    policy = PasswordPolicy.from_names(
        length = 6,
        numbers = 1
    )

    # lupa password
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', location = 'json', required = True)

        args = parser.parse_args()
        
        qry = Users.query.filter_by(email = args['email'])
        data_user = qry.first()

        if data_user is not None:
            return {'message' : 'Cek email untuk mengubah password anda'}, 200

        return{'message' : 'email tidak terdaftar'}, 401

    # ubah password
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('password_lama', location = 'json', required = True)
        parser.add_argument('password_baru', location = 'json', required = True)
        parser.add_argument('konfirmasi_password', location = 'json', required = True)

        args = parser.parse_args()

        claims = get_jwt_claims()
        encrypted_password = hashlib.md5(args['password_lama'].encode()).hexdigest()

        qry = Users.query.filter_by(username = claims['username']).filter_by(password = encrypted_password)
        data_user = qry.first()

        if data_user is not None:
            validation = self.policy.test(args['password_baru'])
            if validation:
                list_error = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    list_error.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Mohon cek password baru anda: " + ', '.join(x for x in list_error)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            elif args['password_baru'] != args['konfirmasi_password']:
                return {'message': 'Konfirmasi password tidak sesuai'}, 401

            encrypted = hashlib.md5(args['password_baru'].encode()).hexdigest()
            data_user.password = encrypted
            db.session.commit()

            return {'message' : 'ubah password berhasil'}, 200
        else:       
            return {'message' : 'password salah'}, 404

    def options(self, id=None):
        return {'status':'ok'},200
        
api.add_resource(PasswordResources,'')