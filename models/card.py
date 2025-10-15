"""
This file defines the model for the 'cards' table and it's relationships. 
"""
# Built-in imports
import enum

# Local imports
from init import db


"""
Enumerated values for attributes of a card that have a value from a 
pre-defined set
"""

class CardType(enum.Enum):
    """
    This defines the unique type of card that can be found printed on the 
    top of the card. This assumes a card has only one type.
    """
    Digiegg = "digiegg"
    Digimon = "digimon"
    Option = "option"
    Tamer = "tamer"

class CardRarity(enum.Enum):
    """
    This is the print rarity of the card and also determines the 
    distribution and likelihood of opening them in a box. This is found at 
    the bottom of the card near the traits.
    """
    Common = "common"
    Uncommon = "uncommon"
    Rare = "rare"
    SuperRare = "super_rare"
    SecretRare = "secret_rare"

class Card(db.Model):
    """
    The card table template. This contains the columns for the atomic features
    that define what a card is:
        - Card number
        - Card name
        - Card type
        - Card Rarity
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "cards"

    # Table columns
    card_id = db.Column(db.Integer, primary_key = True)
    card_number = db.Column(db.String(), nullable = False)
    card_name = db.Column(db.String(), nullable = False)
    card_type = db.Column(db.Enum(CardType), nullable = False)
    card_rarity = db.Column(db.Enum(CardRarity), nullable = False)

    """
    Define the relationship between cards and the decks they are put in.
    A decklist can't exist if there are no cards in the deck.
    """
    # Delete decklists associated to the card when they are deleted
    decklists = db.relationship(
        "Decklist", 
        back_populates = "card", 
        cascade = "all, delete"
    )