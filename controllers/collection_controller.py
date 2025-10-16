"""
This file creates the Create, Read, Update, and Delete operations 
to the collection data, through REST API design using Flask 
Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.collection import Collection
from schemas.schemas import collection_schema, collections_schema

# Create the Template Web Application Interface for card routes 
# to be applied to the Flask application
collectionsBp = Blueprint("collections", __name__, url_prefix = "/collections")


"""
Collection Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No records found. Add a statement to get started."
    }, 404

def error_collection_does_not_exist(collection_id):
    return {
        "message": 
        f"Collection ID {collection_id} does not exist in this table."
    }, 404

def deck_sucessfully_delete_from_collection(player_id, deck_id):
    return {
        "message": 
        f"Deck ID {deck_id} has been removed from Player ID {player_id}'s collection."
    }, 200 


"""
API Routes
"""

@collectionsBp.route("/", methods = ["POST"])
def create_collection():
    """
    Retrieve the body data and add the details of the collection 
    into the collection database, this is the equivalent of POST 
    in postgresql. This is how we add cards into a deck.
    """
    # Fetch the collection information from the request body
    bodyData = request.get_json()

    # Create a new entry into the deck using the request body data 
    # and the collection schema will organise the data to their 
    # matching attributes with validation rules implemented.
    addDeckToCollection = Collection(
        player_id = bodyData.get("player_id"),
        deck_id = bodyData.get("deck_id")    
    )
    
    # Add the collection data into the session
    db.session.add(addDeckToCollection)
    
    # Commit and write the collection data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(collection_schema.dump(addDeckToCollection)), 201


@collectionsBp.route("/")
def get_collections():
    """
    Retrieve and read all the collections from the collections 
    database, this is the equivalent of GET in postgresql.
    """
    # Select all the collections from the database and the cards 
    # that are in these decks
    collection_id = request.args.get("collection_id", type = int)
    player_id = request.args.get("player_id", type = int)
    deck_id = request.args.get("deck_id", type = int)
    statement = db.select(Collection)
    
    # Display collections that exist
    if collection_id:
        statement = statement.where(Collection.collection_id == collection_id)

    # Display players that have a collection
    if player_id:
        statement = statement.where(Collection.player_id == player_id)
    
    # Display decks that exist in those players' collections
    if deck_id:
        statement = statement.where(Collection.deck_id == deck_id)

    # Serialise it as the scalar result is unserialised
    collections_list = db.session.scalars(statement)
    queryData = collections_schema.dump(collections_list)

    # Return the search results if there are collections in the 
    # collection database, otherwise inform the user that the 
    # database is empty.
    if queryData:
        # Return the list of collections in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Collections table is empty
        return error_empty_table()
    

@collectionsBp.route("/<int:collection_id>", methods = ["DELETE"])
def delete_deck_from_collection(collection_id):
    """
    Find the deck in the player's collection with the matching IDs 
    and remove it from the collections database. This is the 
    equivalent of DELETE in postgresql.
    """
    # Selects all the collections from the database and filter for 
    # the deck with matching ID
    statement = db.select(Collection).where(Collection.collection_id == collection_id)
    
    # Serialise it as the scalar result is unserialised
    collection = db.session.scalar(statement)
    queryData = collection_schema.dump(collection)

    # Delete the collection from the collections database if they exist
    if queryData:
        player_id = queryData["player_id"]
        deck_id = queryData["deck_id"]

        # Remove the collection from the session
        db.session.delete(collection)
        
        # Commit and permanently remove the collection data from 
        # the postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return deck_sucessfully_delete_from_collection(player_id, deck_id)
    else:
        # Return an error message: Collection with this ID does 
        # not exist
        return error_collection_does_not_exist(collection_id)