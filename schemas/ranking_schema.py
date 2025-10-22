"""
This file creates the structure on how ranking data should be 
organised within our relational database, their constraints, 
and the relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates

# Local imports - Tables
from models.ranking import Ranking


class RankingSchema(SQLAlchemyAutoSchema):
    """
    The ranking schema template. This organises the JSON response 
    when fetching ranking information such as the event a player is 
    attending to, the player playing at the event, and their 
    performance at the event.
    """
    class Meta:
        model = Ranking
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Player Info, Event Info, Personal Performance Info
        fields = (
            "player_id",
            "players", 
            "event_id",
            "events",
            "placement",
            "points",
            "wins",
            "losses",
            "ties"
        )

    # Only show the name of the player when showing player 
    # information in the ranking query
    players = fields.Nested(
        "PlayerSchema", 
        only = (
            "player_name",
        )
    )

    # Only show the name of the card and unique card number when 
    # showing card information in the ranking query
    events = fields.Nested(
        "EventSchema", 
        only = (
            "event_name",
        )
    )

    # Only show the name of the deck when showing deck information in
    # the ranking query
    decks = fields.Nested(
        "DeckSchema", 
        only = (
            "deck_name",
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
ranking_schema = RankingSchema()
rankings_schema = RankingSchema(many = True)