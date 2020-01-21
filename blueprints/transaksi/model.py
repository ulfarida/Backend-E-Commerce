from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta

class Transaksi(db.Model):
    __tablename__ = "Transaksi"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)
    nama_penerima = db.Column(db.String(255), nullable = False)
    no_hp_penerima = db.Column(db.String(20), nullable = False)
    alamat_pengiriman = db.Column(db.String(1000), nullable = False)
    metode_pembayaran = db.Column(db.String(255), nullable = False)
    jasa_kirim = db.Column(db.String(255), nullable = False)
    harga = db.Column(db.Integer, nullable = False)
    ongkos_kirim = db.Column(db.Integer, nullable = False)
    diskon = db.Column(db.Integer, nullable = False)
    total_harga = db.Column(db.Integer, nullable = False)
    status = db.Column(db.String(255), nullable = False, default='belum dibayar')
    deleted = db.Column(db.Boolean, nullable = False, default=False)

    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'nama_penerima' : fields.String,
        'no_hp_penerima' : fields.String,
        'alamat_pengiriman' : fields.String,
        'metode_pembayaran' : fields.String,
        'jasa_kirim' : fields.String,
        'harga' : fields.Integer,
        'ongkos_kirim' : fields.Integer,
        'diskon' : fields.Integer,
        'total_harga' : fields.Integer,
        'status' : fields.String,
        'deleted' : fields.Boolean
    }

    def __init__(self, user_id, nama_penerima, no_hp_penerima, alamat_pengiriman, metode_pembayaran, jasa_kirim, harga, ongkos_kirim, diskon, total_harga):
        self.user_id = user_id
        self.nama_penerima = nama_penerima
        self.no_hp_penerima = no_hp_penerima
        self.alamat_pengiriman = alamat_pengiriman
        self.metode_pembayaran = metode_pembayaran
        self.jasa_kirim = jasa_kirim
        self.harga = harga
        self.ongkos_kirim = ongkos_kirim
        self.diskon = diskon
        self.total_harga = total_harga

    def __repr__(self):
        return '<Transaksi %r>' %self.id

class TransaksiDetails(db.Model):
    __tablename__ = "TransaksiDetails"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    transaksi_id = db.Column(db.Integer, db.ForeignKey("Transaksi.id"), nullable = False)
    produk_id = db.Column(db.Integer, db.ForeignKey("Produk.id"), nullable = False)
    kuantitas = db.Column(db.Integer, nullable = False, default=1)
    harga = db.Column(db.Integer, nullable = False)

    response_fields = {
        'id' : fields.Integer,
        'transaksi_id' : fields.Integer,
        'produk_id' : fields.Integer,
        'kuantitas' : fields.Integer,
        'harga' : fields.Integer
    }

    def __init__(self, transaksi_id, produk_id, kuantitas, harga):
        self.transaksi_id = transaksi_id
        self.produk_id = produk_id
        self.kuantitas = kuantitas
        self.harga = harga

    def __repr__(self):
        return '<TransaksiDetails %r>' %self.id