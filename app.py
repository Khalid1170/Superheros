from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower  # Import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize the database with the app

# Routes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = []
    
    for hero in heroes:
        heroes_data.append({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        })
    
    return jsonify(heroes_data), 200

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': []
        }
        for hero_power in hero.hero_powers:
            power_data = {
                'hero_id': hero_power.hero_id,
                'id': hero_power.id,
                'power': {
                    'description': hero_power.power.description,
                    'id': hero_power.power.id,
                    'name': hero_power.power.name
                },
                'power_id': hero_power.power_id,
                'strength': hero_power.strength
            }
            hero_data['hero_powers'].append(power_data)
        return jsonify(hero_data), 200
    return jsonify({"error": "Hero not found"}), 404


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = []
    for power in powers:
        powers_data.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })
    return jsonify(powers_data), 200

@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power:
        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        }), 200
    return jsonify({"error": "Power not found"}), 404

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            }), 200
        return jsonify({'errors': ['Validation errors']}), 400
    return jsonify({"error": "Power not found"}), 404

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['Validation errors']}), 400
    
    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero and power:
        new_hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
        db.session.add(new_hero_power)
        db.session.commit()

        return jsonify({
            'id': new_hero_power.id,
            'hero_id': new_hero_power.hero_id,
            'power_id': new_hero_power.power_id,
            'strength': new_hero_power.strength,
            'hero': {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            },
            'power': {
                'description': power.description,
                'id': power.id,
                'name': power.name
            }
        }), 201
    return jsonify({'errors': ['Validation errors']}), 400

if __name__ == '__main__':
    app.run(debug=True)
