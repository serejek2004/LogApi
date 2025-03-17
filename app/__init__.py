from flask import Flask
from app.config import Config
from app.database import db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from app.user import controller
from app.log import controller
