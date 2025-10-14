"""
This file defines the model for the 'decks' table and it's relationships. 
"""
# Local imports
from init import db

class Deck(db.Model):
    """
    The deck table template. This contains the name of a deck and the 
    relationships between decklists, player collections, and decks.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "decks"

    # Table columns
    deck_id = db.Column(db.Integer, primary_key = True)
    deck_name = db.Column(db.String(), nullable = False)