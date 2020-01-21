from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json, datetime, hashlib
from . import *
from blueprints import db, app
from blueprints.keranjang.model import Keranjang, KeranjangDetails
from blueprints.produk.model import Produk
from blueprints.transaksi.model import Transaksi, TransaksiDetails
from blueprints.transaksi.model import Transaksi
from flask_jwt_extended  import jwt_required, verify_jwt_in_request, get_jwt_claims

bp_checkout = Blueprint('checkout',__name__)
api = Api(bp_checkout)

class CheckoutResources(Resource):

    # checkout semua produk di keranjang
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama_penerima', location = 'json', required = True)
        parser.add_argument('no_hp_penerima', location = 'json', required = True)
        parser.add_argument('alamat_pengiriman', location = 'json', required = True)
        parser.add_argument('metode_pembayaran', location = 'json', required = True)
        parser.add_argument('jasa_kirim', location = 'json', required = True)
        parser.add_argument('voucher', location = 'json', required = False)
        args = parser.parse_args()

        claims = get_jwt_claims()
        qry_keranjang = Keranjang.query.filter_by(user_id = claims['id'])
        keranjang_data = qry_keranjang.first()

        qry_keranjang_details = KeranjangDetails.query.filter_by(keranjang_id = keranjang_data.id).filter_by(deleted=False)

        # list semua produk yang ingin dicheckout
        produks = []
        for produk in qry_keranjang_details:
            item = marshal(produk, KeranjangDetails.response_fields)
            produks.append(item)

        #membuat transaksi
        if produks is not None:
            transaksi = Transaksi(claims['id'], args['nama_penerima'], 
                        args['no_hp_penerima'], args['alamat_pengiriman'],
                        args['metode_pembayaran'], args['jasa_kirim'], harga=0,
                        ongkos_kirim=0, diskon=0, total_harga=0)
            db.session.add(transaksi)
            db.session.commit()
            app.logger.debug('DEBUG : %s', transaksi)

            #membuat transaksi detail (list produk)
            qry_transaksi = Transaksi.query.filter_by(user_id = claims['id']).filter_by(harga=0).filter_by(deleted=False)
            qry_transaksi = qry_transaksi.first()
            for produk in produks:
                qry_produk = Produk.query.get(produk['produk_id'])
                if qry_produk.stok >= produk['kuantitas']:
                    qry_produk.stok -= produk['kuantitas']
                    qry_produk.jumlah_terjual += produk['kuantitas']
                    qry_transaksi.harga += produk['harga']
                    qry_transaksi.total_harga += produk['harga']

                    transaksi_detail = TransaksiDetails(qry_transaksi.id, produk['produk_id'], produk['kuantitas'], produk['harga'])
                    db.session.add(transaksi_detail)
                    db.session.commit()

                    app.logger.debug('DEBUG : %s', transaksi_detail)

                else:
                    return {'message' : 'kuantitas pembelian melebihi stok yang tersedia'}

            #menghapus produk pada keranjang yang berhasil di checkout
            qry_keranjang_details_2 = qry_keranjang_details.filter_by(deleted=False)
            for qry in qry_keranjang_details_2:
                qry.deleted = True
                db.session.commit()
                
            keranjang_data.total_harga = 0
            
            db.session.commit()


            return {'message' : "checkout berhasil"}, 200

    def options(self):
        return {}, 200

api.add_resource(CheckoutResources,'')