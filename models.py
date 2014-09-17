from flask import Flask
from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    hash_password = db.Column(db.String(128))    

    def __init__(self, username, password, name=None, email=None):
        self.username = username
        self.hash_password = pwd_context.encrypt(password)
        if name is not None:
            self.name = name

        if email is not None:
            self.email = email

    def verify_password(self, password):
        return pwd_context.verify(password, self.hash_password)

    def set_password(self, password):
        self.hash_password = pwd_context.encrypt(password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username
