
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, validates
from sqlalchemy import ForeignKey
from sqlalchemy_serializer import SerializerMixin 

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    hero_powers = relationship('HeroPower', back_populates='hero', cascade='all, delete')

    serialize_rules = ('-hero_powers.hero',)

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False) 

    hero_powers = relationship('HeroPower', back_populates='power', cascade='all, delete')

    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, value):
        if len(value) < 20:
            raise ValueError('Description must be at least 20 characters long.')
        return value

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(50), nullable=False)  
    hero_id = db.Column(db.Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, ForeignKey('powers.id'), nullable=False)

    hero = relationship('Hero', back_populates='hero_powers')
    power = relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if value not in valid_strengths:
            raise ValueError(f"Strength must be one of {valid_strengths}")
        return value
