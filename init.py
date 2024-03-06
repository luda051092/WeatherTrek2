from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config  # Import the Config class from config.py

app = Flask(__name__)
app.config.from_object(Config)  # Set the configuration from Config class
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from user import user_bp
from .weather_routes import weather_bp
from .city_routes import city_bp

app.register_blueprint(user_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(city_bp, url_prefix='')

from . import user  # Importing user module after app creation

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
