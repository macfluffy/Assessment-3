"""
This file creates the structure on how the data should be organised within our relational database,
their constraints, and the relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

# Local imports - Tables
from models.card import Card

class CardSchema(SQLAlchemyAutoSchema):
    """
    The card schema template. This organises the JSON response when fetching card
    information such as the card's name, number, type and rarity.
    """
    class Meta:
        model = Card
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Name, Enrolments, Contact Details
        fields = (
            "card_id", 
            "card_number", 
            "card_name", 
            "card_type", 
            "card_rarity"
        )

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
card_schema = CardSchema()
cards_schema = CardSchema(many = True)