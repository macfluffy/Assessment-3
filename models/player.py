"""
This file defines the model for the 'players' table and it's relationships. 
"""
# Local imports
from init import db

class Player(db.Model):
    """
    The deck table template. This contains the name of a player and the 
    relationships between the player collections, rankings, and tournament 
    registrations.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "players"

    # Table columns
    player_id = db.Column(db.Integer, primary_key = True)
    player_name = db.Column(db.String(), nullable = False)