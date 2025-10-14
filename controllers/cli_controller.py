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
    Populate the table with initial data. Card information is added 
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