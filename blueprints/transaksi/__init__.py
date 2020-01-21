from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.transaksi.model import Transaksi, TransaksiDetails
from blueprints.produk.model import Produk
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_transaksi = Blueprint('transaksi',__name__)
api = Api(bp_transaksi)

class TransaksiResources(Resource):

    # lihat transaksi (user)
    @jwt_required
    def get(self):

        claims = get_jwt_claims()
        qry_transaksi = Transaksi.query.filter_by(user_id = claims['id']).filter_by(deleted=False)

        if qry_transaksi is not None:
            list_transaksi = []
            for transaksi in qry_transaksi:
                marshal_transaksi = marshal(transaksi, Transaksi.response_fields)
                list_transaksi.append(marshal_transaksi)

            return list_transaksi, 200

    def options(self):
        return {}, 200
class TransaksiDetailResources(Resource):

    # lihat transaksi detail
    @jwt_required
    def get(self, id):

        qry_transaksi_detail = TransaksiDetails.query.filter_by(transaksi_id = id)

        if qry_transaksi_detail is not None:
            list_produk = []
            for produk in qry_transaksi_detail:
                marshal_produk = marshal(produk, TransaksiDetails.response_fields)
                marshal_produk['produk'] = marshal(Produk.query.get(produk.produk_id), Produk.response_fields)
                list_produk.append(marshal_produk)

            return list_produk, 200

    def options(self):
        return {}, 200

api.add_resource(TransaksiResources,'')
api.add_resource(TransaksiDetailResources,'/<int:id>')