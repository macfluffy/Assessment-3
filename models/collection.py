"""
This file defines the model for the 'collection' junction table and it's 
relationships with 'decks' and the 'players' models. 
"""

# Local imports - The Flask App instance (db)
from init import db # References app created on initialisation

class Collection(db.Model):
    """
    The collection table template contains the information about a player
    and all the decks they own (and registered into this database). A  
    collection cannot exist without a player to populate it with their 
    decks.
    """
    
    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "collections"

    # Table columns
    # collection_id refers to a specific deck belonging to a specific player
    collection_id = db.Column(db.Integer, primary_key = True) 
    player_id = db.Column(
        db.Integer, 
        db.ForeignKey("players.player_id"), 
        nullable = False
    )
    deck_id = db.Column(
        db.Integer, 
        db.ForeignKey("decks.deck_id"), 
        nullable = False
    )

    """
    A collection is a players' stash of owned decks. Create the constraints 
    and relationships between this table and the other tables to reflect 
    this behaviour.
    """
    # Create a unique constraint that prevents duplicate decks in a player's 
    # collection
    __table_args__ = (
        db.UniqueConstraint(
            "player_id", 
            "deck_id", 
            name = "unique_decks_in_player_collection"
        ),
    )

    # Define the relationships between players, decks, and collections
    player = db.relationship("Player", back_populates = "collections")
    deck = db.relationship("Deck", back_populates = "collections")