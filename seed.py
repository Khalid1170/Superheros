from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")

        # Clear existing data from the HeroPower, Power, and Hero tables
        db.session.query(HeroPower).delete()  # Deletes all hero-power associations
        db.session.query(Power).delete()  # Deletes all power entries
        db.session.query(Hero).delete()  # Deletes all hero entries

        print("Seeding powers...")
        # Define a list of powers with their names and descriptions
        powers = [
            Power(name="Super Strength", description="Grants the wielder immense strength, capable of lifting heavy objects and overpowering enemies."),
            Power(name="Flight", description="Allows the wielder to fly at high speeds and navigate through the air effortlessly."),
            Power(name="Superhuman Senses", description="Enhances the wielder's senses, allowing them to perceive things beyond human capability."),
            Power(name="Elasticity", description="Grants the ability to stretch and reshape one's body into various forms."),
        ]
        # Add the powers to the session
        db.session.add_all(powers)

        print("Seeding heroes...")
        # Define a list of heroes with their real names and superhero names
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]
        # Add the heroes to the session
        db.session.add_all(heroes)

        print("Assigning powers to heroes...")
        # List of strengths for each hero-power relationship
        strengths = ["Strong", "Weak", "Average"]
        # Randomly assign powers to heroes, and assign random strength values
        hero_powers = [HeroPower(hero=rc(heroes), power=rc(powers), strength=rc(strengths)) for _ in range(10)]

        # Add the hero-power relationships to the session
        db.session.add_all(hero_powers)
        
        # Commit all changes to the database
        db.session.commit()

        print("✅ Done seeding!")
