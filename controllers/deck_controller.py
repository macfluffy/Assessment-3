"""
This file creates the Create, Read, Update, and Delete operations to our deck data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.deck import Deck
from schemas.deck_schema import deck_schema, decks_schema

# Create the Template Web Application Interface for deck routes to be applied 
# to the Flask application
decksBp = Blueprint("decks", __name__, url_prefix = "/decks")


"""
Deck Controller Messages
"""

def error_empty_table():
    return {"message": "No decks found in this database. Add a deck to get started."}

def error_deck_does_not_exist(deck_id):
    return {"message": f"Deck with id {deck_id} does not exist"}, 404

def deck_successfully_removed(deck_name):
    return {"message": f"{deck_name} deck deleted successfully."}, 200 


"""
API Routes
"""

@decksBp.route("/", methods = ["POST"])
def createDeck():
    """
    Retrieve the body data and add the details of the deck into the deck database,
    this is the equivalent of POST in postgresql.
    """
    # Fetch the deck information from the request body
    bodyData = request.get_json()
    
    # Create a new deck object with the request body data as the attributes
    # using validation rules in the schema
    newDeck = deck_schema.load(
        bodyData,
        session = db.session
    )

    # Add the deck data into the session
    db.session.add(newDeck)
    
    # Commit and write the deck data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = deck_schema.dump(newDeck)
    return jsonify(acknowledgement), 201


@decksBp.route("/")
def getDecks():
    """
    Retrieve and read all the decks from the deck database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the decks from the database
    statement = db.select(Deck)
    listOfDecks = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = decks_schema.dump(listOfDecks)
    
    # Return the search results if there are decks in the deck database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of decks in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Deck table is empty
        return error_empty_table()
    

@decksBp.route("/<int:deck_id>")
def getDeck(deck_id):
    """
    Retrieve and read a specific deck's information from 
    the deck database, using the deck ID as the marker.
    """
    # Selects all the decks from the database and filter the deck with
    # matching ID
    statement = db.select(Deck).where(Deck.deck_id == deck_id)
    deck = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = deck_schema.dump(deck)

    # Return the search results if this deck is in the deck database, 
    # otherwise inform the user that the deck does not exist.
    if queryData:
        # Return the deck info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Deck with this ID does not exist
        return error_deck_does_not_exist(deck_id)
    

@decksBp.route("/<int:deck_id>", methods = ["PUT", "PATCH"])
def updateDeck(deck_id):
    """
    Retrieve the body data and update the details of the deck with the 
    matching ID in the deck database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the decks from the database and filter the deck with
    # matching ID
    statement = db.select(Deck).where(Deck.deck_id == deck_id)
    deck = db.session.scalar(statement)

    # Update the deck information in the decks database if they exist
    if deck:
        # Fetch the deck information from the request body
        bodyData = request.get_json()

        # Update the deck's details with these new changes, otherwise 
        # reuse the same information
        deck.deck_name = bodyData.get("deck_name", deck.deck_name)
        
        # Commit and permanently update the deck data in the 
        # postgresql database
        db.session.commit()

        # Return the updated deck info in JSON format
        return jsonify(deck_schema.dump(deck))
    else:
        # Return an error message: Deck with this ID does not exist
        return error_deck_does_not_exist(deck_id)
    

@decksBp.route("/<int:deck_id>", methods = ["DELETE"])
def deleteDeck(deck_id):
    """
    Find the deck with the matching ID in the deck database and remove them.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the decks from the database and filter the deck with
    # matching ID
    statement = db.select(Deck).where(Deck.deck_id == deck_id)
    deck = db.session.scalar(statement)

    # Delete the deck from the decks database if they exist
    if deck:
        # Remove the deck from the session
        db.session.delete(deck)
        
        # Commit and permanently remove the deck data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return deck_successfully_removed(deck.deck_name)
    else:
        # Return an error message: Deck with this ID does not exist
        return error_deck_does_not_exist(deck_id)