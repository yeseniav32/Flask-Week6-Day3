# Standard
import uuid
from datetime import datetime
import secrets
#3rd party imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
#Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User Model Creation
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(50), nullable = True, default = '')
    last_name = db.Column(db.String(50), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = "owner", lazy = True)

    def __init__(self, email, first_name = '', last_name='', id='',password='',token='',g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self,length):
        return secrets.token_hex(length)

    
    def __repr__(self):
        return f'User {self.email} has been added to the database.'

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(50))
    price = db.Column(db.Numeric(precision=10, scale=2))
    features = db.Column(db.String(250), nullable = True)
    engine = db.Column(db.String(100), nullable = True)
    technologies = db.Column(db.String(150))
    wheels = db.Column(db.String(100))
    safety = db.Column(db.String(100))
    dimension = db.Column(db.String(100))
    fuel_economy = db.Column(db.String(100))
    accessories = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, price, features, engine, technologies, wheels, safety, dimension, fuel_economy, 
                accessories, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.price = price
        self.features = features
        self.engine = engine
        self.technologies = technologies
        self.wheels = wheels
        self.safety = safety
        self.dimension = dimension
        self.fuel_economy = fuel_economy
        self.accessories = accessories
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f"The following Drone has been created: {self.name}."

# Creation of API Schema via Marshmallow Object
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id','name','price','features','engine','technologies','wheels','safety',
                'dimension','fuel_economy','accessories']
                
car_schema = CarSchema()
cars_schema = CarSchema(many=True)