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

    """
    Define the relationship between cards and the decks they are put in.
    A decklist can't exist if the deck if it does not have a name.
    """
    # Delete decklists associated to the card when they are deleted
    decklists = db.relationship(
        "Decklist", 
        back_populates = "deck", 
        cascade = "all, delete"
    )