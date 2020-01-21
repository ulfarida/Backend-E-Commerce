from flask import Blueprint, request
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.user.model import Users, UserDetails
import json, hashlib
from password_strength import PasswordPolicy
from blueprints import db, app

bp_profil = Blueprint('profil',__name__)
api = Api(bp_profil)

class ProfilResources(Resource):

    # edit profil 
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location = 'json', required = False)
        parser.add_argument('alamat', location = 'json', required = False)
        parser.add_argument('no_hp', location = 'json', required = False)
        parser.add_argument('tanggal_lahir', location = 'json', required = False)
        parser.add_argument('foto_profil', location = 'json', required = False)

        args = parser.parse_args()
        
        claims = get_jwt_claims()

        qry = UserDetails.query.filter_by(user_id = claims['id'])
        data_user = qry.first()

        if args['nama'] is not None:
            data_user.nama = args['nama']
        if args['alamat'] is not None:
            data_user.alamat = args['alamat']
        if args['no_hp'] is not None:
            data_user.no_hp = args['no_hp']
        if args['tanggal_lahir'] is not None:
            data_user.tanggal_lahir = args['tanggal_lahir']
        if args['foto_profil'] is not None:
            data_user.foto_profil = args['foto_profil']

        db.session.commit()

        return{'message' : 'edit profil berhasil'}, 200


    # lihat profil 
    @jwt_required
    def get(self):        
        claims = get_jwt_claims()

        qry = UserDetails.query.filter_by(user_id = claims['id'])
        data_user = qry.first()

        profil = marshal(data_user, UserDetails.response_fields)

        return profil, 200

    def options(self):
        return {}, 200


        
api.add_resource(ProfilResources,'')