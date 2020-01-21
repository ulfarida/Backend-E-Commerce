from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.user.model import Users, UserDetails
from blueprints.keranjang.model import Keranjang
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims
from password_strength import PasswordPolicy

bp_register = Blueprint('register',__name__)
api = Api(bp_register)

class RegisterResource(Resource):
    policy = PasswordPolicy.from_names(
        length = 6,
        numbers = 1
    )

    # register account
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location = 'json', required = True)
        parser.add_argument('email', location = 'json', required = True)
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('confirm_password', location = 'json', required = True)
        args = parser.parse_args()
        
        if args['password'] != args['confirm_password']:
            return {'message': 'Konfirmasi password tidak sesuai'}, 401
        else:
            validation = self.policy.test(args['password'])
            if validation:
                list_error = []
                for item in validation:
                    split = str(item).split('(')
                    error, num = split[0], split[1][0]
                    list_error.append("{err}(minimum {num})".format(err=error, num=num))
                message = "Please check your password: " + ', '.join(x for x in list_error)
                return {'message': message}, 422, {'Content-Type': 'application/json'}
            encrypted = hashlib.md5(args['password'].encode()).hexdigest()

            user = Users(args['username'], args['email'], encrypted)
            db.session.add(user)
            try:
                db.session.commit()
            except Exception as e:
                return {'message': 'username atau email sudah terdaftar'}, 401
            app.logger.debug('DEBUG : %s', user)

            qry = Users.query.filter_by(username = args['username'])
            data_user = qry.first()

            profil = UserDetails(data_user.id, None, None, None, args['email'], None, None)
            db.session.add(profil)
            db.session.commit()
            app.logger.debug('DEBUG : %s', profil)

            keranjang = Keranjang(user_id = data_user.id, total_harga = 0)
            db.session.add(keranjang)
            db.session.commit()
            app.logger.debug('DEBUG : %s', keranjang)

            return {'message' : "registrasi berhasil, silakan login untuk proses selanjutnya"},200,{'Content-Type': 'application/json'}

    def options(self, id=None):
        return {'status':'ok'},200
        
api.add_resource(RegisterResource,'')