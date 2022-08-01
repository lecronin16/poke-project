from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False, unique=True)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    # collect = db.relationship("CollectPokemon", backref ="owner", lazy=True)
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

# class PokeTeam(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     poke1 = db.Column(db.String(50), nullable=False)
#     poke2 = db.Column(db.String(50), nullable=False)
#     poke3 = db.Column(db.String(50), nullable=False)
#     poke4 = db.Column(db.String(50), nullable=False)
#     poke5 = db.Column(db.String(50), nullable=False)

#     # foreign keys
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def __init__(self, poke1, poke2, poke3, poke4, poke5, user_id):
#         self.poke1 = poke1
#         self.poke2 = poke2
#         self.poke3 = poke3
#         self.poke4 = poke4
#         self.poke5 = poke5
#         self.user_id = user_id