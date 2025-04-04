from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin 

# Initialize the database
db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    # Define the 'heroes' table
    __tablename__ = 'heroes'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Hero's real name
    super_name = db.Column(db.String(100), nullable=False)  # Hero's alias (superhero name)

    # Define the relationship with HeroPower table
    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete')

    # Serialization rules (exclude hero field in hero_powers)
    serialize_rules = ('-hero_powers.hero',)

class Power(db.Model, SerializerMixin):
    # Define the 'powers' table
    __tablename__ = 'powers'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name of the power (e.g., "Flight")
    description = db.Column(db.String(255), nullable=False)  # Description of the power

    # Define the relationship with HeroPower table
    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete')

    # Serialization rules (exclude power field in hero_powers)
    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, value):
        # Validate description length to ensure it has at least 20 characters
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long.')
        return value

class HeroPower(db.Model, SerializerMixin):
    # Define the 'hero_powers' table (many-to-many relationship between Hero and Power)
    __tablename__ = 'hero_powers'

    # Define columns
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    strength = db.Column(db.String(50), nullable=False)  # Strength of the power (e.g., "Strong")
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'), nullable=False)  # Foreign key to Hero
    power_id = db.Column(db.Integer, ForeignKey('powers.id'), nullable=False)  # Foreign key to Power

    # Define the relationships with Hero and Power tables
    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    # Serialization rules (exclude hero_powers in both hero and power relationships)
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        # Validate strength value to ensure it is one of the allowed values
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}")
        return value
