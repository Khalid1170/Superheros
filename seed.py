from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")

        # Clear existing data
        db.session.query(HeroPower).delete()
        db.session.query(Power).delete()
        db.session.query(Hero).delete()

        print("Seeding powers...")
        powers = [
            Power(name="Super Strength", description="Grants the wielder immense strength, capable of lifting heavy objects and overpowering enemies."),
            Power(name="Flight", description="Allows the wielder to fly at high speeds and navigate through the air effortlessly."),
            Power(name="Superhuman Senses", description="Enhances the wielder's senses, allowing them to perceive things beyond human capability."),
            Power(name="Elasticity", description="Grants the ability to stretch and reshape one's body into various forms."),
        ]
        db.session.add_all(powers)

        print("Seeding heroes...")
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
        db.session.add_all(heroes)

        print("Assigning powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = [HeroPower(hero=rc(heroes), power=rc(powers), strength=rc(strengths)) for _ in range(10)]

        db.session.add_all(hero_powers)
        db.session.commit()
        print("✅ Done seeding!")
