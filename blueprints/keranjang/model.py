from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta

class Keranjang(db.Model):
    __tablename__ = "Keranjang"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)
    total_harga = db.Column(db.Integer, nullable = False, default=0)

    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'total_harga' : fields.Integer
    }

    def __init__(self, user_id, total_harga):
        self.user_id = user_id
        self.total_harga = total_harga

    def __repr__(self):
        return '<Keranjang %r>' %self.id

class KeranjangDetails(db.Model):
    __tablename__ = "KeranjangDetails"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    keranjang_id = db.Column(db.Integer, db.ForeignKey("Keranjang.id"), nullable = False)
    produk_id = db.Column(db.Integer, db.ForeignKey("Produk.id"), nullable = False)
    kuantitas = db.Column(db.Integer, nullable = False, default=1)
    harga = db.Column(db.Integer, nullable = False)
    deleted = db.Column(db.Boolean, nullable = False, default=False)

    response_fields = {
        'id' : fields.Integer,
        'keranjang_id' : fields.Integer,
        'produk_id' : fields.Integer,
        'kuantitas' : fields.Integer,
        'harga' : fields.Integer
    }

    def __init__(self, keranjang_id, produk_id, kuantitas, harga):
        self.keranjang_id = keranjang_id
        self.produk_id = produk_id
        self.kuantitas = kuantitas
        self.harga = harga

    def __repr__(self):
        return '<KeranjangDetails %r>' %self.id