"""
This file creates the structure on how deck data should be 
organised within the relational database, their constraints, and 
the relationships between decks, cards, and decklists.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp
from marshmallow import fields

# Local imports - Tables
from models.deck import Deck


class DeckSchema(SQLAlchemyAutoSchema):
    """
    The deck schema template. This organises the JSON response when 
    fetching deck information such as the deck's name.
    """
    class Meta:
        model = Deck
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Deck Name
        fields = (
            "deck_id", 
            "deck_name"
        )

    # A deck must have a name
    deck_name = auto_field(
        validate = [
            Length(
                min = 1,
                error = "A deck must have a name and cannot be blank."
            ), Regexp(
                r"[^\s]",
                error = "A deck name cannot start with a blank."
            )
        ]
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
deck_schema = DeckSchema()
decks_schema = DeckSchema(many = True)