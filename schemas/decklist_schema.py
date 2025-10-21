"""
This file creates the structure on how decklist data should be 
organised within the relational database, their constraints, and 
the relationships between decks, cards, and decklists.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates

# Local imports - Tables
from models.decklist import Decklist


class DecklistSchema(SQLAlchemyAutoSchema):
    """
    The decklist schema template. This organises the JSON response when 
    fetching decklist information such as how many copies of a card are 
    in this list, and the name of the deck.
    """
    class Meta:
        model = Decklist
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Deck Info, Card Info, Card Quantity
        fields = (
            "deck_id",
            "decks",
            "card_quantity",
            "card_id", 
            "cards"
        )

    # Only show the name of the deck when showing deck information in
    # the decklist query
    decks = fields.Nested(
        "DeckSchema", 
        only = (
            "deck_name",
        )
    )

    # Only show the name of the card and unique card number when 
    # showing card information in the decklist query
    cards = fields.List(
        fields.Nested(
            "CardSchema", 
            only = (
                "card_number", 
                "card_name"
            )
        )
    )

    # At least 1 copy of a card needs to be added to the decklist
    @validates('card_quantity')
    def validate_cards_added(self, card_quantity, data_key):
        if card_quantity < 1:
            raise ValidationError("At least 1 copy of this card needs to be added into the decklist.")

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
decklist_schema = DecklistSchema()
decklists_schema = DecklistSchema(many = True)