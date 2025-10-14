"""
This file creates the structure on how the data should be organised within our relational database,
their constraints, and the relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

# Local imports - Tables
from models.card import Card
from models.deck import Deck
from models.player import Player
from models.organiser import Organiser
from models.venue import Venue

class CardSchema(SQLAlchemyAutoSchema):
    """
    The card schema template. This organises the JSON response when fetching card
    information such as the card's name, number, type and rarity.
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

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
card_schema = CardSchema()
cards_schema = CardSchema(many = True)


class DeckSchema(SQLAlchemyAutoSchema):
    """
    The deck schema template. This organises the JSON response when fetching deck
    information such as the deck's name.
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

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
deck_schema = DeckSchema()
decks_schema = DeckSchema(many = True)


class PlayerSchema(SQLAlchemyAutoSchema):
    """
    The player schema template. This organises the JSON response when fetching player
    information such as the player's name.
    """
    class Meta:
        model = Player
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Player Name
        fields = (
            "player_id", 
            "player_name"
        )

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
player_schema = PlayerSchema()
players_schema = PlayerSchema(many = True)


class OrganiserSchema(SQLAlchemyAutoSchema):
    """
    The organiser schema template. This organises the JSON response when fetching 
    organiser information such as the organiser's name, and contact details.
    """
    class Meta:
        model = Organiser
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Organiserer Name, Email, and Phone Number
        fields = (
            "organiser_id", 
            "organiser_name",
            "organiser_email",
            "organiser_number"
        )

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
organiser_schema = OrganiserSchema()
organisers_schema = OrganiserSchema(many = True)


class VenueSchema(SQLAlchemyAutoSchema):
    """
    The venue schema template. This organises the JSON response when fetching 
    venue information such as the venue's name, location and contact details.
    """
    class Meta:
        model = Venue
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Venue Name, Address, and Phone Number
        fields = (
            "organiser_id", 
            "organiser_name",
            "organiser_email",
            "organiser_number"
        )

# Create instances of the schema for the controllers to call when applying validation,
# error handling and restrictions
venue_schema = VenueSchema()
venues_schema = VenueSchema(many = True)