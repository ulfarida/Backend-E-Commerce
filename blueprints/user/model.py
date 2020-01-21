from blueprints import db
from flask_restful import fields
from datetime import datetime, timedelta

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(180), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

    response_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        'password': fields.String
    }

    jwt_claims_fields = {
        'id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        # 'isadmin' : fields.Boolean
    }

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Users %r>' %self.id

class UserDetails(db.Model):
    __tablename__ = "UserDetails"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = False)
    nama = db.Column(db.String(255), nullable = True)
    alamat = db.Column(db.String(1000), nullable = True)
    no_hp = db.Column(db.String(20), nullable = True)
    email = db.Column(db.String(255), nullable = False)
    tanggal_lahir = db.Column(db.Date, nullable = True)
    foto_profil = db.Column(db.String(1000), nullable = True)

    response_fields = {
        'id' : fields.Integer,
        'user_id' : fields.Integer,
        'nama' : fields.String,
        'alamat': fields.String,
        'no_hp': fields.String,
        'email': fields.String,
        'tanggal_lahir': fields.String,
        'foto_profil': fields.String
    }

    def __init__(self, user_id, nama, alamat, no_hp, email, tanggal_lahir, foto_profil):
        self.user_id = user_id
        self.nama = nama
        self.alamat = alamat
        self.no_hp = no_hp
        self.email = email
        self.tanggal_lahir = tanggal_lahir
        self.foto_profil = foto_profil

    def __repr__(self):
        return '<UserDetails %r>' %self.id
