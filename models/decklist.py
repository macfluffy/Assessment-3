"""
This file defines the model for the 'decklist' junction table and it's 
relationships with 'decks' and the 'cards' models. 
"""

# Local imports
from init import db

class Decklist(db.Model):
    """
    The decklist table template contains the information about a deck's
    makeup of cards. Decks cannot exist without a card to populate it 
    and a name for the collection of these cards.
    """
    
    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "decklists"
    
    # Table columns
    deck_id = db.Column(
        db.Integer, 
        db.ForeignKey("decks.deck_id"), 
        nullable = False
    )
    card_id = db.Column(
        db.Integer, 
        db.ForeignKey("cards.card_id"), 
        nullable = False
    )
    card_quantity = db.Column(
        db.Integer,
        default = 1,
        nullable = False
    )

    """
    A decklist is comprised of a number of cards combined together under
    a collective name for the deck. As such decks must contain at least
    1 of an included card, and decklists needs cards to be associated 
    with a deck.
    """
    # Define the primary key as a union of both the deck_id and card_id
    __table_args__ = (
        db.PrimaryKeyConstraint(
            "deck_id", 
            "card_id", 
            name = "deck_build"
        ),
        db.CheckConstraint('card_quantity > 0') # at least 1 copy
    )

    # Define the relationships between cards, decks, and decklists
    deck = db.relationship("Deck", back_populates = "decklists")
    card = db.relationship("Card", back_populates = "decklists")