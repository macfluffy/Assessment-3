"""
This file creates the structure on how registration data should be 
organised within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp
from marshmallow import fields

# Local imports - Registration table template
from models.registration import Registration


class RegistrationSchema(SQLAlchemyAutoSchema):
    """
    The registration schema template. This organises the JSON response when 
    fetching registration information such as the event a player is 
    attending to, the player signing in, and the deck they plan to use at 
    the event
    """
    class Meta:
        model = Registration
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Event Info, Player Info, Deck Info, Registration Info
        fields = (
            "event_id",
            "events",
            "player_id",
            "players", 
            "registered_deck",
            "decks",
            "registration_date"
        )

    # Only show the name of the card and unique card number when 
    # showing card information in the registration query
    events = fields.Nested(
        "EventSchema", 
        only = (
            "event_name",
        )
    )

    # Only show the name of the player when showing player 
    # information in the registration query
    players = fields.Nested(
        "PlayerSchema", 
        only = (
            "player_name",
        )
    )

    # Only show the name of the deck when showing deck information in
    # the registration query
    decks = fields.Nested(
        "DeckSchema", 
        only = (
            "deck_name",
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
registration_schema = RegistrationSchema()
registrations_schema = RegistrationSchema(many = True)