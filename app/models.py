from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


#create a flask table:

pokeCollection = db.Table('pokeCollection',
    db.Column('caught_id', db.Integer, db.ForeignKey('pokemon.id')),
    db.Column('caughtby_id', db.Integer, db.ForeignKey('user.id')),
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    # pokemon = db.Column(db.Integer, db.ForeignKey('pokemon.id'))
    pokeCollection = db.relationship("Pokemon",
        # primaryjoin = (pokeCollection.c.caughtby_id == id),
        # secondaryjoin = (pokeCollection.c.caught_id == id),
        secondary = pokeCollection,
        backref = "pokemon_owner",
        lazy= 'dynamic')


    def __init__(self,username,email,password):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def updateUserInfo(self, username, email, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.email = email

    def saveUpdates(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def catchPokemon(self, caught):
        self.pokeCollection.append(caught)
        db.session.commit()

    def releasePokemon(self, let_go):
        self.pokeCollection.delete(let_go)
        db.session.commit()

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon = db.Column(db.String(250), unique=True)
    ability = db.Column(db.String(250))
    img_url = db.Column(db.String(250))
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)

    def __init__(self,pokemon, ability, img_url, hp, attack, defense):
        self.pokemon = pokemon
        self.ability = ability
        self.img_url = img_url
        self.hp = hp
        self.attack = attack
        self.defense = defense

# class PokeCollection(db.Model):
#     pokemon_collection_id = db.Column(db.Integer, primary_key=True)
#     pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'), nullable = False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

#     def __init__(self, pokemon_id, user_id):
#         self.pokemon_id = pokemon_id
#         self.user_id = user_id