from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta

class Wishlist(db.Model):
    __tablename__ = "Wishlist"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)
    produk_id = db.Column(db.Integer, db.ForeignKey("Produk.id"), nullable = False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    response_fields = {
        # 'id' : fields.Integer,
        # 'user_id' : fields.Integer,
        'produk_id' : fields.Integer
    }

    def __init__(self, user_id, produk_id):
        self.user_id = user_id
        self.produk_id = produk_id

    def __repr__(self):
        return '<Wishlist %r>' %self.id