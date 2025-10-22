"""
This file creates the structure on how card data should be 
organised within the relational database, their constraints, and 
the relationships between cards, decks, and decklists.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, OneOf, Regexp
from marshmallow import fields

# Local imports - Tables & Enums
from models.card import Card, CardType, CardRarity


class CardSchema(SQLAlchemyAutoSchema):
    """
    The card schema template. This organises the JSON response when 
    fetching card information such as the card's name, number, type 
    and rarity.
    """
    class Meta:
        model = Card
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Card Number, Card Name, Type, and Rarity
        fields = (
            "card_id", 
            "card_number", 
            "card_name", 
            "card_type", 
            "card_rarity"
        )

    # Card must have a collection number
    card_number = auto_field(
        validate = [
            Length(
                min = 1,
                error = "Card cannot have a blank number"
            ), Regexp(
                r"[^\s]",
                error = "Card number cannot start with a blank."
            )
        ]
    )

    # Card's must not be blank
    card_name = auto_field(
        validate = [
            Length(
                min = 1,
                error = "Card cannot have a blank name."
            ), Regexp(
                r"[^\s]",
                error = "A card's name cannot start with a blank."
            )
        ]
    )

    # Cards are defined by the following types: Digiegg, Digimon,
    # Option, and Tamer. They must contain one of these types.
    card_type = auto_field(
        validate = OneOf(
            [
                CardType.Digiegg,
                CardType.Digimon,
                CardType.Option,
                CardType.Tamer
            ],
            error = "Only valid card types are allowed. Digiegg, Digimon, Option, or Tamer."
        )
    )

    # Cards have a rarity. It must be one of the following: Common,
    # Uncommon, Rare, Super Rare, or Secret Rare.
    card_rarity = auto_field(
        validate = OneOf(
            [
                CardRarity.Common,
                CardRarity.Uncommon,
                CardRarity.Rare,
                CardRarity.SuperRare,
                CardRarity.SecretRare
            ],
            error = "Only valid card rarities are allowed. Common, Uncommon, Rare, Super Rare, or Secret Rare."
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
card_schema = CardSchema()
cards_schema = CardSchema(many = True)