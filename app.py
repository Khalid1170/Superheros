from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Hero, Power, HeroPower  # Import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
db.init_app(app)  # Initialize the database with the app

# Route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()  # Fetch all heroes from the database
    heroes_data = []
    
    # Prepare hero data for the response
    for hero in heroes:
        heroes_data.append({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        })
    
    return jsonify(heroes_data), 200  # Return the heroes data as JSON

# Route to get a hero by their ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)  # Fetch hero by ID from the database
    if hero:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': []
        }
        
        # Add hero powers to the response data
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
        
        return jsonify(hero_data), 200  # Return hero data with associated powers
    return jsonify({"error": "Hero not found"}), 404  # Return error if hero not found

# Route to get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()  # Fetch all powers from the database
    powers_data = []
    
    # Prepare power data for the response
    for power in powers:
        powers_data.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })
    return jsonify(powers_data), 200  # Return the powers data as JSON

# Route to get a power by its ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)  # Fetch power by ID from the database
    if power:
        return jsonify({
            'id': power.id,
            'name': power.name,
            'description': power.description
        }), 200  # Return power data
    return jsonify({"error": "Power not found"}), 404  # Return error if power not found

# Route to update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)  # Fetch power by ID from the database
    if power:
        data = request.get_json()  # Get the JSON data from the request
        if 'description' in data:
            power.description = data['description']  # Update the power's description
            db.session.commit()  # Commit the changes to the database
            return jsonify({
                'id': power.id,
                'name': power.name,
                'description': power.description
            }), 200  # Return updated power data
        return jsonify({'errors': ['Validation errors']}), 400  # Return error if validation fails
    return jsonify({"error": "Power not found"}), 404  # Return error if power not found

# Route to create a new hero-power association
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()  # Get the JSON data from the request
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    # Validate strength input
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'errors': ['Validation errors']}), 400
    
    hero = Hero.query.get(hero_id)  # Fetch the hero by ID
    power = Power.query.get(power_id)  # Fetch the power by ID

    # Check if both the hero and power exist in the database
    if hero and power:
        new_hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)  # Create new hero-power association
        db.session.add(new_hero_power)  # Add the new association to the session
        db.session.commit()  # Commit the changes to the database

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
        }), 201  # Return the newly created hero-power association data
    return jsonify({'errors': ['Validation errors']}), 400  # Return error if validation fails

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
