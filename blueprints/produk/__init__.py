from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.produk.model import Produk
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_produk = Blueprint('produk',__name__)
api = Api(bp_produk)

class ProdukResources(Resource):

    # lihat seluruh produk
    def get(self):   
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']) - args['rp']

        qry_produk = Produk.query.filter_by(deleted = False)

        produks = []
        for produk in qry_produk.limit(args['rp']).offset(offset).all():
            semua_produk = marshal(produk, Produk.response_fields)
            produks.append(semua_produk)

        return produks, 200

    def options(self):
        return {}, 200

class ProdukbyIdResources(Resource):

    # lihat produk by id
    def get(self, id):

        qry = Produk.query.filter_by(id = id).filter_by(deleted=False)
        item_produk = qry.first()

        if item_produk is not None:
            return marshal(item_produk, Produk.response_fields), 200
        else:
            return {'message' : 'produk tidak ditemukan'}, 404

    def options(self):
        return {}, 200

api.add_resource(ProdukResources,'')
api.add_resource(ProdukbyIdResources, '/<int:id>')