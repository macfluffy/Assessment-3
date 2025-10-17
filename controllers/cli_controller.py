"""
This file creates the Create, Read, Update, and Delete operations to our command
line interface through REST API design using Flask Blueprint. This file creates
the commands to automate the creation and seeding of the LMS database.
"""

# Installed import packages
from flask import Blueprint

# Local imports
from init import db
from models.card import Card, CardRarity, CardType
from models.deck import Deck
from models.player import Player
from models.organiser import Organiser
from models.venue import Venue
from models.decklist import Decklist
from models.collection import Collection
from models.event import Event, EventStatus
from models.registration import Registration

# Create the Template Application Interface for in-line command routes to be applied 
# to the Flask application
dbCommands = Blueprint("db", __name__)


"""
API Routes
"""

@dbCommands.cli.command("create")
def createTables():
    """
    Creates all the tables as defined in the models subfolder
    """
    db.create_all()
    print("Tables created.")


@dbCommands.cli.command("drop")
def dropTables():
    """
    This function deletes all tables and leaves an empty database
    """
    db.drop_all()
    print("Tables dropped.")

@dbCommands.cli.command("seed")
def seed_tables():
    """
    Populate the table with initial data. Card and deck information is added 
    into the LMS database.
    """
    # Create cards to add to the cards database
    cards = [Card(
        card_number = "BT1-001",
        card_name = "Yokomon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Rare
    ), Card(
        card_number = "BT1-002",
        card_name = "Bebydomon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Uncommon
    ), Card(
        card_number = "BT1-003",
        card_name = "Upamon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Rare
    ), Card(
        card_number = "BT1-004",
        card_name = "Wanyamon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Uncommon
    ), Card(
        card_number = "BT1-005",
        card_name = "Kyaromon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Uncommon
    ), Card(
        card_number = "BT1-006",
        card_name = "Cupimon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Rare
    ), Card(
        card_number = "BT1-007",
        card_name = "Tanemon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Rare
    ), Card(
        card_number = "BT1-008",
        card_name = "Frimon",
        card_type = CardType.Digiegg,
        card_rarity = CardRarity.Uncommon
    ), Card(
        card_number = "BT1-009",
        card_name = "Monodramon",
        card_type = CardType.Digimon,
        card_rarity = CardRarity.Common
    ), Card(
        card_number = "BT1-010",
        card_name = "Agumon",
        card_type = CardType.Digimon,
        card_rarity = CardRarity.Rare
    )]

    # Add the card information to this session
    db.session.add_all(cards)

    # Commit to the session and permanently add the cards to the 
    # database.
    db.session.commit()
    print("Cards table has been seeded.")

    # Create decks to add to the decks database
    decks = [Deck(
        deck_name = "WarGreymon"
        ), Deck(
            deck_name = "Rookie Rush"
        ), Deck(
            deck_name = "Birds"
        )]
    
    # Add the deck information to this session
    db.session.add_all(decks)

    # Commit to the session and permanently add the decks to the 
    # database.
    db.session.commit()
    print("Decks table has been seeded.")

    # Create players to add to the players database
    players = [Player(
        player_name = "macflurry"
        ), Player(
            player_name = "Snippythelucky"
        ), Player(
            player_name = "Faker"
        )]
    
    # Add the player information to this session
    db.session.add_all(players)

    # Commit to the session and permanently add the players to the 
    # database.
    db.session.commit()
    print("Players table has been seeded.")

    # Create organisers to add to the organisers database
    organisers = [Organiser(
        organiser_name = "Tak Games",
        organiser_email = "events@takgames.com.au",
        organiser_number = "0298513267"
        ), Organiser(
            organiser_name = "Bandai",
            organiser_email = "oceanicevents@bandai.com.au",
            organiser_number = "0385423125"
        ), Organiser(
            organiser_name = "Card Gamerz",
            organiser_email = "bob@cardgamerz.com.au",
            organiser_number = "0297731234"
        )]
    
    # Add the organiser information to this session
    db.session.add_all(organisers)

    # Commit to the session and permanently add the organisers to the 
    # database.
    db.session.commit()
    print("Organisers table has been seeded.")

    # Create venues to add to the venues database
    venues = [Venue(
        venue_name = "Sydney International Convention Centre",
        venue_address = "14 Darling Dr, Sydney NSW 2000",
        venue_number = "0292157100"
        ), Venue(
            venue_name = "Marvel Stadium",
            venue_address = "740 Bourke St, Docklands VIC 3008",
            venue_number = "0386257700"
        ), Venue(
            venue_name = "Qudos Bank Arena",
            venue_address = "19 Edwin Flack Ave, Sydney Olympic Park NSW 2127",
            venue_number = "0287654321"
        )]
    
    # Add the venue information to this session
    db.session.add_all(venues)

    # Commit to the session and permanently add the venues to the 
    # database.
    db.session.commit()
    print("Venues table has been seeded.")

    decklists = [Decklist(
        deck_id = decks[0].deck_id,
        card_id = cards[0].card_id,
        card_quantity = 3
    ), Decklist(
        deck_id = decks[0].deck_id,
        card_id = cards[1].card_id,
        card_quantity = 4
    )]

    # Add the decklist information to this session
    db.session.add_all(decklists)

    # Commit to the session and permanently add the decklists to the 
    # database.
    db.session.commit()
    print("Decklists seeded.")

    collections = [Collection(
        player_id = players[0].player_id,
        deck_id = decks[0].deck_id
    ), Collection(
        player_id = players[0].player_id,
        deck_id = decks[1].deck_id
    ), Collection(
        player_id = players[1].player_id,
        deck_id = decks[0].deck_id
    ), Collection(
        player_id = players[1].player_id,
        deck_id = decks[1].deck_id
    ), Collection(
        player_id = players[2].player_id,
        deck_id = decks[0].deck_id
    ), Collection(
        player_id = players[2].player_id,
        deck_id = decks[1].deck_id
    )]

    # Add the collections information to this session
    db.session.add_all(collections)

    # Commit to the session and permanently add the collections to the 
    # database.
    db.session.commit()
    print("Collection seeded.")

    events = [Event(
        organiser_id = organisers[0].organiser_id,
        venue_id = venues[1].venue_id,
        event_name = "BandaiFest 2025",
        player_cap = 255,
        event_date = "2025-10-10",
        event_details = "Celebrate the 25th anniversary of Digimon!",
        event_status = EventStatus.Completed
    ), Event(
        organiser_id = organisers[1].organiser_id,
        venue_id = venues[0].venue_id,
        event_name = "Digimon Sydney Regionals 2025",
        player_cap = 128,
        event_date = "2025-12-10",
        event_details = "Compete to represent Australia at World's 2025!",
        event_status = EventStatus.Planned
    ), Event(
        organiser_id = organisers[2].organiser_id,
        venue_id = venues[2].venue_id,
        event_name = "Pax Games",
        player_cap = 32,
        event_date = "2025-10-16",
        event_details = "Check out the latest in gaming news!",
        event_status = EventStatus.Running
    ), Event(
        organiser_id = organisers[0].organiser_id,
        venue_id = venues[0].venue_id,
        event_name = "Games Expo 2025",
        player_cap = 32,
        event_date = "2025-09-10",
        event_details = "Latest in games!",
        event_status = EventStatus.Cancelled
    )]

    # Add the events information to this session
    db.session.add_all(events)

    # Commit to the session and permanently add the events to the 
    # database.
    db.session.commit()
    print("Event seeded.")

    registrations = [Registration(
        event_id = events[2].event_id,
        player_id = players[1].player_id,
        registered_deck = collections[2].collection_id,
        registration_date = "2025-10-08"
    ), Registration(
        event_id = events[2].event_id,
        player_id = players[0].player_id,
        registered_deck = collections[0].collection_id,
        registration_date = "2025-10-13"
    ), Registration(
        event_id = events[2].event_id,
        player_id = players[2].player_id,
        registered_deck = collections[5].collection_id,
        registration_date = "2025-10-09"
    ), Registration(
        event_id = events[1].event_id,
        player_id = players[2].player_id,
        registered_deck = collections[5].collection_id,
        registration_date = "2025-10-10"
    )]

    # Add the registrations information to this session
    db.session.add_all(registrations)

    # Commit to the session and permanently add the registrations to the 
    # database.
    db.session.commit()
    print("Registration seeded.")