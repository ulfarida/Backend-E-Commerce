from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.keranjang.model import Keranjang, KeranjangDetails
from blueprints.produk.model import Produk
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_keranjang = Blueprint('keranjang',__name__)
api = Api(bp_keranjang)

class KeranjangResources(Resource):

    # tambah produk ke keranjang
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('produk_id', location = 'json', required = True)
        parser.add_argument('kuantitas', location = 'json', required = True)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry = Keranjang.query.filter_by(user_id = claims['id'])
        data_keranjang = qry.first()

        qry_produk = Produk.query.filter_by(id = args['produk_id']).filter_by(deleted=False)
        data_produk = qry_produk.first()

        if data_produk is not None:
            if int(args['kuantitas']) > data_produk.stok :
                return {'message' : "kuantitas melebihi stok yang tersedia"}, 401
            else:
                harga = data_produk.harga * int(args['kuantitas'])
                data_keranjang.total_harga += harga
                
                qry_keranjang_details = KeranjangDetails.query.filter_by(keranjang_id = data_keranjang.id).filter_by(deleted=False)
                for item in qry_keranjang_details:
                    if int(args['produk_id']) == item.produk_id:
                        item.kuantitas += int(args['kuantitas'])
                        item.harga += harga
                        db.session.commit()
                        return {'message' : "produk berhasil ditambahkan ke keranjang!"}, 200

                produk = KeranjangDetails(data_keranjang.id, args['produk_id'], args['kuantitas'], harga)
                db.session.add(produk)
                db.session.commit()
                app.logger.debug('DEBUG : %s', produk)

                return {'message' : "produk berhasil ditambahkan ke keranjang!"},200
        else:
            return {'message' : "produk tidak ditemukan"},200

    # lihat seluruh produk di keranjang
    @jwt_required
    def get(self):   
        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=25)
        args = parser.parse_args()

        offset = (args['p']*args['rp']) - args['rp']

        claims = get_jwt_claims()

        qry_keranjang = Keranjang.query.filter_by(user_id = claims['id'])
        data_keranjang = qry_keranjang.first()

        qry_keranjang_details = KeranjangDetails.query.filter_by(keranjang_id = data_keranjang.id).filter_by(deleted=False)

        if qry_keranjang_details is not None:
            produks = []
            for produk in qry_keranjang_details:
                marshal_produk = marshal(produk, KeranjangDetails.response_fields)
                marshal_produk['produk'] = marshal(Produk.query.get(marshal_produk['produk_id']), Produk.response_fields)
                produks.append(marshal_produk)

        keranjang_info = marshal(data_keranjang, Keranjang.response_fields)
        keranjang_info['produk'] = produks
        return keranjang_info, 200

    def options(self):
        return {}, 200

class KeranjangbyIdResources(Resource):

    # hapus produk dari keranjang
    @jwt_required
    def delete(self, id):        
        claims = get_jwt_claims()

        qry_keranjang = Keranjang.query.filter_by(user_id = claims['id'])
        data_keranjang = qry_keranjang.first()

        qry_keranjang_details = KeranjangDetails.query.filter_by(keranjang_id = data_keranjang.id).filter_by(deleted=False).filter_by(id = id)
        item_produk = qry_keranjang_details.first()

        if item_produk is not None:
            item_produk.deleted = True
            data_keranjang.total_harga -= item_produk.harga
            db.session.commit()
            return {'message' : 'produk telah terhapus dari keranjang'}, 200
        else:
            return {'message' : 'produk tidak ditemukan'}, 404

    #edit kuantitas keranjang details
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('kuantitas', location = 'json', required = False)
        args = parser.parse_args()


        qry_keranjang_details = KeranjangDetails.query.get(id)

        if qry_keranjang_details is not None:
            qry_produk = Produk.query.filter_by(id = qry_keranjang_details.produk_id).filter_by(deleted=False)
            data_produk = qry_produk.first()
            if args['kuantitas'] is not None:
                qry_keranjang_details.kuantitas = args['kuantitas']
                harga_awal = qry_keranjang_details.harga
                harga_akhir = data_produk.harga * int(args['kuantitas'])
                qry_keranjang_details.harga = harga_akhir
                Keranjang.query.get(qry_keranjang_details.keranjang_id).total_harga += (harga_akhir - harga_awal)

            db.session.commit()
            return {'message' : 'edit keranjang berhasil'}, 200

        else:
            return {'message' : 'keranjang tidak ditemukan'}, 404

    def options(self):
        return {}, 200

api.add_resource(KeranjangResources,'')
api.add_resource(KeranjangbyIdResources, '/<int:id>')