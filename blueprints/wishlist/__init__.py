from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.produk.model import Produk
from blueprints.wishlist.model import Wishlist
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_wishlist = Blueprint('wishlist',__name__)
api = Api(bp_wishlist)

class WishlistResources(Resource):

    # tambah produk ke wishlist
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('produk_id', location = 'json', required = True)
        args = parser.parse_args()

        claims = get_jwt_claims()

        qry_produk = Produk.query.filter_by(id = args['produk_id']).filter_by(deleted=False)
        data_produk = qry_produk.first()

        if data_produk is not None:        
            qry_wishlist = Wishlist.query.filter_by(user_id = claims['id']).filter_by(deleted=False)

            for item in qry_wishlist:
                if int(args['produk_id']) == item.produk_id:
                    return {'message' : "produk sudah masuk wishlist"}, 200

            produk = Wishlist(claims['id'], args['produk_id'])
            db.session.add(produk)
            db.session.commit()
            app.logger.debug('DEBUG : %s', produk)

            return {'message' : "produk berhasil ditambahkan ke wishlist!"},200
        else:
            return {'message' : "produk tidak ditemukan"},200


    # lihat seluruh produk di wishlist
    @jwt_required
    def get(self):   
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']) - args['rp']

        claims = get_jwt_claims()

        qry_wishlist = Wishlist.query.filter_by(user_id = claims['id']).filter_by(deleted=False)

        if qry_wishlist is not None:
            produks = []
            for produk in qry_wishlist:
                marshal_produk = marshal(produk, Wishlist.response_fields)
                marshal_produk['detail_produk'] = marshal(Produk.query.get(marshal_produk['produk_id']), Produk.response_fields)
                produks.append(marshal_produk)

            return produks, 200
        
        else :
            {'message' : 'tidak ada produk dalam wishlist'}, 200

    # hapus produk dari wishlist
    @jwt_required
    def delete(self, id):        
        claims = get_jwt_claims()

        qry_wishlist = Wishlist.query.filter_by(user_id = claims['id']).filter_by(deleted=False).filter_by(id=id)
        item_produk = qry_wishlist.first()

        if item_produk is not None:
            item_produk.deleted = True
            db.session.commit()
            return {'message' : 'produk telah terhapus dari wishlist'}, 200
        else:
            return {'message' : 'produk tidak ditemukan'}, 404

    def options(self):
        return {}, 200

api.add_resource(WishlistResources,'', '/<int:id>')