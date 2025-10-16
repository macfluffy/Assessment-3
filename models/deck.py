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
    Define the special relationships:
      - Decklist: A decklist can't be referenced if the deck does not 
                  have a name.
      - Collection: A player's collection needs to have decks in it
                    to be considered a collection.
    """
    # Delete the decklist associated to this deck when they are deleted
    decklists = db.relationship(
        "Decklist", 
        back_populates = "deck", 
        cascade = "all, delete"
    )
    # Delete this deck in all players' collections when deleted
    collections = db.relationship(
        "Collection",
        back_populates = "deck",
        cascade = "all, delete"
    )