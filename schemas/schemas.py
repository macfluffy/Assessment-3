"""
This file creates the structure on how the data should be organised 
within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates

# Local imports - Tables
from models.card import Card
from models.deck import Deck
from models.player import Player
from models.organiser import Organiser
from models.venue import Venue
from models.decklist import Decklist
from models.collection import Collection
from models.event import Event
from models.registration import Registration
from models.ranking import Ranking

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

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
card_schema = CardSchema()
cards_schema = CardSchema(many = True)


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

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
deck_schema = DeckSchema()
decks_schema = DeckSchema(many = True)


class PlayerSchema(SQLAlchemyAutoSchema):
    """
    The player schema template. This organises the JSON response when 
    fetching player information such as the player's name.
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

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
player_schema = PlayerSchema()
players_schema = PlayerSchema(many = True)


class OrganiserSchema(SQLAlchemyAutoSchema):
    """
    The organiser schema template. This organises the JSON response when 
    fetching organiser information such as the organiser's name, and 
    contact details.
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

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
organiser_schema = OrganiserSchema()
organisers_schema = OrganiserSchema(many = True)


class VenueSchema(SQLAlchemyAutoSchema):
    """
    The venue schema template. This organises the JSON response when 
    fetching venue information such as the venue's name, location 
    and contact details.
    """
    class Meta:
        model = Venue
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Venue Name, Address, and Phone Number
        fields = (
            "venue_id", 
            "venue_name",
            "venue_address",
            "venue_number"
        )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
venue_schema = VenueSchema()
venues_schema = VenueSchema(many = True)


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


class CollectionSchema(SQLAlchemyAutoSchema):
    """
    The collection schema template. This organises the JSON response when 
    fetching collection information such as the decks in a players' 
    collection.
    """
    class Meta:
        model = Collection
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Player ID, Deck ID
        fields = (
            "collection_id",
            "player_id",
            "players",
            "deck_id",
            "decks"
        )

    # Only show the name of the player when showing player 
    # information in the collection query
    players = fields.Nested(
        "PlayerSchema", 
        only = (
            "player_name",
        )
    )

    # Only show the name of the deck when showing deck information in
    # the collection query
    decks = fields.Nested(
        "DeckSchema", 
        only = (
            "deck_name",
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many = True)


class EventSchema(SQLAlchemyAutoSchema):
    """
    The event schema template. This organises the JSON response when 
    fetching event information such as the organiser, venue, details
    about the event, and the player caps.
    """
    class Meta:
        model = Event
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Event ID, Organiser ID, Venue ID, Event Details
        fields = (
            "event_id",
            "organiser_id",
            "organisers",
            "venue_id",
            "venues",
            "event_name",
            "player_cap",
            "event_date",
            "event_details",
            "event_status"
        )

    # Only show the name of the organiser when showing organiser 
    # information in the event query
    organisers = fields.Nested(
        "OrganiserSchema", 
        only = (
            "organiser_name",
        )
    )

    # Only show the name of the venue when showing venue information in
    # the event query
    venues = fields.Nested(
        "VenueSchema", 
        only = (
            "venue_name",
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
event_schema = EventSchema()
events_schema = EventSchema(many = True)


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


class RankingSchema(SQLAlchemyAutoSchema):
    """
    The ranking schema template. This organises the JSON response when 
    fetching ranking information such as the event a player is 
    attending to, the player playing at the event, and their performance
    at the event.
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