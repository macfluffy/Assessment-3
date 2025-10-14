"""
Using app factory design method for handling 
"""

# Built-in imports
import os

# Installed import packages
from flask import Flask
from dotenv import load_dotenv

# Local imports
from init import db
from controllers.cli_controller import dbCommands
from controllers.card_controller import cardsBp

load_dotenv()

def create_app():
    """
    Create a single instance of the Flask application which will be called from
    the rest of the code.
    """

    # Create the instance of the flask app
    app = Flask(__name__)
    print("Flask server started.")
    
    # Load the database address from the .env file. This function requires 
    # load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    
    # Keep the order of keys in JSON response
    app.json.sort_keys = False
    db.init_app(app)
    
    # Apply the imported routes created in the controllers folder to this 
    # instance of Flask app
    app.register_blueprint(dbCommands)
    app.register_blueprint(cardsBp)
    return app