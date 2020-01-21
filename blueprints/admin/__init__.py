from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app, admin_required
from blueprints.produk.model import Produk
from blueprints.user.model import Users, UserDetails
from blueprints.transaksi.model import Transaksi, TransaksiDetails
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_admin = Blueprint('admin',__name__)
api = Api(bp_admin)

class ProdukAdminResources(Resource):

    def options(self, *args, **kwargs):
        return {'status':'ok'},200

    # tambah produk
    @jwt_required
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location = 'json', required = True)
        parser.add_argument('foto_produk', location = 'json', required = True)
        parser.add_argument('kategori', location = 'json', required = True)
        parser.add_argument('harga', location = 'json', required = True)
        parser.add_argument('stok', location = 'json', required = True)
        parser.add_argument('deskripsi', location = 'json', required = False)
        parser.add_argument('lokasi', location = 'json', required = False)
        args = parser.parse_args()
        
        produk = Produk(args['nama_produk'], args['foto_produk'], args['kategori'], args['harga'], args['stok'], args['deskripsi'], args['lokasi'])
        db.session.add(produk)
        db.session.commit()

        app.logger.debug('DEBUG : %s', produk)

        return {'message' : "produk berhasil ditambahkan!"},200


    #edit produk
    @jwt_required
    @admin_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_produk', location = 'json', required = False)
        parser.add_argument('foto_produk', location = 'json', required = False)
        parser.add_argument('kategori', location = 'json', required = False)
        parser.add_argument('harga', location = 'json', required = False)
        parser.add_argument('stok', location = 'json', required = False)
        parser.add_argument('deskripsi', location = 'json', required = False)
        parser.add_argument('lokasi', location = 'json', required = False)
        args = parser.parse_args()


        qry = Produk.query.filter_by(id = id).filter_by(deleted= False)
        produkItem = qry.first()

        if produkItem is not None:
            if args['nama_produk'] is not None:
                produkItem.nama_produk = args['nama_produk']
            if args['foto_produk'] is not None:
                produkItem.foto_produk = args['foto_produk']
            if args['kategori'] is not None:
                produkItem.kategori = args['kategori']
            if args['harga'] is not None:
                produkItem.harga = args['harga']
            if args['stok'] is not None:
                produkItem.stok = args['stok']
            if args['deskripsi'] is not None:
                produkItem.deskripsi = args['deskripsi']
            if args['lokasi'] is not None:
                produkItem.lokasi = args['lokasi']

            db.session.commit()
            return {'message' : 'edit produk berhasil'}, 200

        else:
            return {'message' : 'produk tidak ditemukan'}, 404

    # hapus produk
    @jwt_required
    @admin_required
    def delete(self, id):        

        qry = Produk.query.filter_by(id = id).filter_by(deleted=False)
        produkItem = qry.first()

        if produkItem is not None:
            produkItem.deleted = True
            db.session.commit()
            return {'message' : 'produk telah terhapus'}, 200
        else:
            return {'message' : 'produk tidak ditemukan'}, 404

class TransaksiAdminResources(Resource):

    # lihat seluruh transaksi
    @jwt_required
    @admin_required
    def get(self):

        qry_transaksi = Transaksi.query.filter_by(deleted = False)

        if qry_transaksi is not None:
            list_transaksi = []
            for transaksi in qry_transaksi:
                marshal_transaksi = marshal(transaksi, Transaksi.response_fields)
                list_transaksi.append(marshal_transaksi)

            return list_transaksi, 200

    #edit status transaksi
    @jwt_required
    @admin_required
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', location = 'json', required = False)
        args = parser.parse_args()

        qry_transaksi = Transaksi.query.filter_by(id = id).filter_by(deleted=False)
        data_transaksi = qry_transaksi.first()

        if data_transaksi is not None:
            if args['status'] is not None:
                data_transaksi.status = args['status']

            db.session.commit()
            return {'message' : 'edit status transaksi berhasil'}, 200

        else:
            return {'message' : 'transaksi tidak ditemukan'}, 404

    #hapus transaksi
    @jwt_required
    @admin_required
    def delete(self, id):
        qry_transaksi = Transaksi.query.filter_by(id = id).filter_by(deleted=False)
        data_transaksi = qry_transaksi.first()

        if data_transaksi is not None:
            data_transaksi.deleted = True

            db.session.commit()
            return {'message' : 'hapus transaksi berhasil'}, 200

        else:
            return {'message' : 'transaksi tidak ditemukan'}, 404

    def options(self):
        return {}, 200

class UserAdminResources(Resource):

    # lihat seluruh transaksi
    @jwt_required
    @admin_required
    def get(self):

        qry_user = Users.query.filter_by(deleted = False)

        if qry_user is not None:
            list_user = []
            for user in qry_user:
                marshal_user = marshal(user, Users.response_fields)
                list_user.append(marshal_user)

            return list_user, 200

    #hapus user
    @jwt_required
    @admin_required
    def delete(self, id):
        qry_user = Users.query.filter_by(id=id).filter_by(deleted = False)
        data_user = qry_user.first()

        if data_user is not None:
            data_user.deleted = True

            db.session.commit()
            return {'message' : 'hapus user berhasil'}, 200

        else:
            return {'message' : 'user tidak ditemukan'}, 404


    def options(self):
        return {}, 200



api.add_resource(ProdukAdminResources,'/produk', '/produk/<int:id>')
api.add_resource(TransaksiAdminResources,'/transaksi', '/transaksi/<int:id>')
api.add_resource(UserAdminResources,'/user', '/user/<int:id>')