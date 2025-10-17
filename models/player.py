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

    """
    Define the special relationships:
      - Collection: A collection belongs to a player. In it is a 
                    collection of their decks.
      - Registration: A player needs to register to attend an 
                      event.
    """
    # Delete this entire player's collection when deleted. No player, 
    # no collection
    collections = db.relationship(
        "Collection",
        back_populates = "player",
        cascade = "all, delete"
    )
    # Delete the registration if the player is deleted
    registrations = db.relationship(
        "Registration",
        back_populates = "player",
        cascade = "all, delete"
    )
    # Delete the ranking if the player is deleted
    rankings = db.relationship(
        "Ranking",
        back_populates = "player",
        cascade = "all, delete"
    )