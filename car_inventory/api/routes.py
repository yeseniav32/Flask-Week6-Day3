from flask import Blueprint, jsonify, request
from flask_login import login_required
from car_inventory.helpers import token_required
from car_inventory.models import db,User,Car,car_schema,cars_schema

api = Blueprint('api',__name__, url_prefix = '/api')

@api.route('getdata')
@token_required
def getdata(current_user_token):
    return jsonify({'some':'value',
                    'Other':44.3})

# Create Drone Route
@api.route('/cars', methods=['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    price = request.json['price']
    features = request.json['features']
    engine = request.json['engine']
    technologies = request.json['technologies']
    wheels = request.json['wheels']
    safety = request.json['safety']
    dimension = request.json['dimension']
    fuel_economy = request.json['fuel_economy']
    accessories = request.json['accessories']
    user_token = current_user_token.token

    car = Car(name,price, features, engine, technologies, wheels, safety,
                dimension, fuel_economy, accessories, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# Retrieve ALL drones
@api.route('/cars', methods=['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# Retrieve a drone
@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_car(current_user_token,id):
    owner = current_user_token.token
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# UPDATE a drone
@api.route('/cars/<id>', methods=['POST','PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.name = request.json['name']
    car.price = request.json['price']
    car.features = request.json['features']
    car.engine = request.json['engine']
    car.technologies = request.json['technologies']
    car.wheels = request.json['wheels']
    car.safety = request.json['safety']
    car.dimension = request.json['dimension']
    car.fuel_economy = request.json['fuel_economy']
    car.accessories = request.json['accessories']
    
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE a drone
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)