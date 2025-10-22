"""
This file creates the Create, Read, Update, and Delete operations to the decklist data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.decklist import Decklist
from schemas.decklist_schema import decklist_schema, decklists_schema

# Create the Template Web Application Interface for card routes to be applied 
# to the Flask application
decklistsBp = Blueprint("decklists", __name__, url_prefix = "/decklists")



"""
Decklist Controller Messages
"""

def error_empty_table():
    return {"message": "No records found. Add a statement to get started."}, 404

def error_decklist_does_not_exist(deck_id, card_id):
    return {"message": f"Card ID {card_id} does not exist in Deck ID {deck_id}."}, 404

def card_sucessfully_delete_from_deck(deck_id, card_id):
    return {"message": f"Card ID {card_id} has been removed from Deck ID {deck_id}."}, 200 


"""
API Routes
"""

@decklistsBp.route("/", methods = ["POST"])
def create_decklist():
    """
    Retrieve the body data and add the details of the decklist into the decklist database,
    this is the equivalent of POST in postgresql. This is how we add cards into a deck.
    """
    # Fetch the decklist information from the request body
    bodyData = request.get_json()

    # Create a new entry into the deck using the request body data and the decklist 
    # schema will organise the data to their matching attributes with validation 
    # rules implemented.
    addCardToDeck = decklist_schema.load(
        bodyData, 
        session = db.session
    )
    
    # Add the decklist data into the session
    db.session.add(addCardToDeck)
    
    # Commit and write the decklist data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(decklist_schema.dump(addCardToDeck)), 201


@decklistsBp.route("/")
def get_decklists():
    """
    Retrieve and read all the decklists from the decklists database,
    this is the equivalent of GET in postgresql.
    """
    # Select all the decklists from the database and the cards that
    # are in these decks
    deck_id = request.args.get("deck_id", type = int)
    card_id = request.args.get("card_id", type = int)
    statement = db.select(Decklist)
    
    # Display decks that exist
    if deck_id:
        statement = statement.where(Decklist.deck_id == deck_id)
    
    # Display cards that exist in these decks
    if card_id:
        statement = statement.where(Decklist.card_id == card_id)

    # Serialise it as the scalar result is unserialised
    decklists_list = db.session.scalars(statement)
    queryData = decklists_schema.dump(decklists_list)

    # Return the search results if there are decklists in the decklist database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of decklists in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Decklists table is empty
        return error_empty_table()
    

@decklistsBp.route("/deck_id=<int:deck_id>&card_id=<int:card_id>", methods = ["DELETE"])
def delete_card_from_decklist(deck_id, card_id):
    """
    Find the card in the deck with the matching IDs and remove it from 
    the decklist database. This is the equivalent of DELETE in 
    postgresql.
    """
    # Selects all the decklists from the database and filter for the deck 
    # with matching ID
    statement = db.select(Decklist).where(Decklist.deck_id == deck_id)
    statement = db.select(Decklist).where(Decklist.card_id == card_id)
    
    # Serialise it as the scalar result is unserialised
    decklist = db.session.scalar(statement)
    queryData = decklist_schema.dump(decklist)

    # Delete the decklist from the decklists database if they exist
    if queryData:
        # Remove the decklist from the session
        db.session.delete(decklist)
        
        # Commit and permanently remove the decklist data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return card_sucessfully_delete_from_deck(deck_id, card_id)
    else:
        # Return an error message: Decklist with this ID does not exist
        return error_decklist_does_not_exist(deck_id, card_id)