from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Address for sale posting will be pulled directly from the the User profile.
    address_1   = db.Column(db.String(140))
    address_2   = db.Column(db.String(140))
    country     = db.Column(db.String(140))
    state       = db.Column(db.String(140))
    postal_code = db.Column(db.String(10))


    # Database Relationship with Sales
    sales = db.relationship('Sale',backref='seller',lazy='dynamic')
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # Sets the password in the database
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # Checks to see if the password entered is correct
    def check_password(self,password):
        # print(password,self.password_hash,generate_password_hash(password))
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Sale(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(140),index=True)
    description = db.Column(db.String(512))
    post_date = db.Column(db.String(140), index=True,default=datetime.utcnow)
    start_date = db.Column(db.String(140), index=True)
    end_date = db.Column(db.String(140), index=True)
    zipcode = db.Column(db.String(10))
    address_1 = db.Column(db.String(140),index=True)
    address_2 = db.Column(db.String(140),index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship('Item',backref='sale',lazy='dynamic')
    # Zip Code, Address (LOCATION)
    def __repr__(self):
        return '<Sale {} {} {}>'.format(self.name,self.post_date,self.user_id)

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(140),index=True)
    description = db.Column(db.String(512),index=True)
    price = db.Column(db.Float(), index=True)
    sale_id = db.Column(db.Integer,db.ForeignKey('sale.id'))