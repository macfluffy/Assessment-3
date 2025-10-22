"""
This file creates the Create, Read, Update, and Delete operations to our card data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.card import Card
from schemas.card_schema import card_schema, cards_schema
# from schemas.schemas import card_schema, cards_schema

# Create the Template Web Application Interface for card routes to be applied 
# to the Flask application
cardsBp = Blueprint("cards", __name__, url_prefix = "/cards")


"""
Card Controller Messages
"""

def error_empty_table():
    return {"message": "No cards found in this database. Add a card to get started."}

def error_card_does_not_exist(card_id):
    return {"message": f"Card with id {card_id} does not exist"}, 404

def card_successfully_removed(card_number, card_name):
    return {"message": f"Card {card_number} {card_name} deleted successfully."}, 200 

"""
API Routes
"""

@cardsBp.route("/", methods = ["POST"])
def createCard():
    """
    Retrieve the body data and add the details of the card into the card database,
    this is the equivalent of POST in postgresql.
    """
    # Fetch the card information from the request body
    bodyData = request.get_json()
    
    # Create a new card object with the request body data as the attributes
    # with validation rules applied
    newCard = card_schema.load(
        bodyData, 
        session = db.session
    )

    # Add the card data into the session
    db.session.add(newCard)
    
    # Commit and write the card data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = card_schema.dump(newCard)
    return jsonify(acknowledgement), 201


@cardsBp.route("/")
def getCards():
    """
    Retrieve and read all the cards from the card database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the cards from the database
    statement = db.select(Card)
    cardsList = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = cards_schema.dump(cardsList)
    
    # Return the search results if there are cards in the card database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of cards in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Card table is empty
        return error_empty_table()
    

@cardsBp.route("/<int:card_id>")
def getCard(card_id):
    """
    Retrieve and read a specific card's information from 
    the card database, using the card ID as the marker.
    """
    # Selects all the cards from the database and filter the card with
    # matching ID
    statement = db.select(Card).where(Card.card_id == card_id)
    card = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = card_schema.dump(card)

    # Return the search results if this card is in the card database, 
    # otherwise inform the user that the card does not exist.
    if queryData:
        # Return the card info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Card with this ID does not exist
        return error_card_does_not_exist(card_id)
    

@cardsBp.route("/<int:card_id>", methods = ["PUT", "PATCH"])
def updateCard(card_id):
    """
    Retrieve the body data and update the details of the card with the 
    matching ID in the card database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the cards from the database and filter the card with
    # matching ID
    statement = db.select(Card).where(Card.card_id == card_id)
    card = db.session.scalar(statement)

    # Update the card information in the cards database if they exist
    if card:
        # Fetch the card information from the request body
        bodyData = request.get_json()

        # Update the card's details with these new changes, otherwise 
        # reuse the same information
        card.card_number = bodyData.get("card_number", card.card_number)
        card.card_name = bodyData.get("card_name", card.card_name)
        card.card_type = bodyData.get("card_type", card.card_type)
        card.card_rarity = bodyData.get("card_rarity", card.card_rarity)
        
        # Commit and permanently update the card data in the 
        # postgresql database
        db.session.commit()
        
        # Return the updated card info in JSON format
        return jsonify(card_schema.dump(card))
    else:
        # Return an error message: Card with this ID does not exist
        return error_card_does_not_exist(card_id)
    

@cardsBp.route("/<int:card_id>", methods = ["DELETE"])
def deleteCard(card_id):
    """
    Find the card with the matching ID in the card database and remove them.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the cards from the database and filter the card with
    # matching ID
    statement = db.select(Card).where(Card.card_id == card_id)
    card = db.session.scalar(statement)

    # Delete the card from the cards database if they exist
    if card:
        # Remove the card from the session
        db.session.delete(card)
        
        # Commit and permanently remove the card data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return card_successfully_removed(card.card_number, card.card_name)
    else:
        # Return an error message: Card with this ID does not exist
        return error_card_does_not_exist(card_id)