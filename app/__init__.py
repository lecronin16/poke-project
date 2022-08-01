from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate

login= LoginManager()

from .auth.auth_routes import auth
from .models import User
from .poketeam.routes import poketeam

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(auth)
app.register_blueprint(poketeam)


from .models import db 

db.init_app(app)
migrate = Migrate(app,db)
login.init_app(app)

from . import routes
from . import models