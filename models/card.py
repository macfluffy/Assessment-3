"""
This file defines the model for the 'cards' table and it's relationships. 
"""

# Local imports
from init import db
import enum

"""
Enumerated values for attributes of a card that have a value from a 
pre-defined set
"""

class CardType(enum.ENUM):
    """
    This defines the unique type of card that can be found printed on the 
    top of the card. This assumes a card has only one type.
    """
    DIGIEGG = "digiegg"
    DIGIMON = "digimon"
    OPTION = "option"
    TAMER = "tamer"

class CardRarity(enum.ENUM):
    """
    This is the print rarity of the card and also determines the 
    distribution and likelihood of opening them in a box. This is found at 
    the bottom of the card near the traits.
    """
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    SUPER_RARE = "super_rare"
    SECRET_RARE = "secret_rare"

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
    card_type = db.Column(db.SqlEnum(CardType), nullable = False)
    card_rarity = db.Column(db.SqlEnum(CardRarity), nullable = False)