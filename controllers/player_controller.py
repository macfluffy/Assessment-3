"""
This file creates the Create, Read, Update, and Delete operations to 
our player data, through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.player import Player
from schemas.player_schema import player_schema, players_schema
# from schemas.schemas import player_schema, players_schema

# Create the Template Web Application Interface for player routes to 
# be applied to the Flask application
playersBp = Blueprint("players", __name__, url_prefix = "/players")


"""
Player Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No players found in this database. Add a player to get started."
    }

def error_player_does_not_exist(player_id):
    return {
        "message": 
        f"Player ID {player_id} does not exist"
    }, 404

def player_successfully_removed(player_name):
    return {
        "message": 
        f"Player {player_name} deleted successfully."
    }, 200 


"""
API Routes
"""

@playersBp.route("/", methods = ["POST"])
def createPlayer():
    """
    Retrieve the body data and add the details of the player into 
    the player database, this is the equivalent of POST in 
    postgresql.
    """
    # Fetch the player information from the request body
    bodyData = request.get_json()
    
    # Create a new player object with the request body data as the 
    # attributes using validation rules in the schema
    newPlayer = player_schema.load(
        bodyData,
        session = db.session
    )

    # newPlayer = Player(
    #     player_name = bodyData.get("player_name")
    # )

    # Add the player data into the session
    db.session.add(newPlayer)
    
    # Commit and write the player data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = player_schema.dump(newPlayer)
    return jsonify(acknowledgement), 201


@playersBp.route("/")
def getPlayers():
    """
    Retrieve and read all the players from the player database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the players from the database
    statement = db.select(Player)
    playersList = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = players_schema.dump(playersList)
    
    # Return the search results if there are players in the player 
    # database, otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of players in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Player table is empty
        return error_empty_table()
    

@playersBp.route("/<int:player_id>")
def getPlayer(player_id):
    """
    Retrieve and read a specific player's information from 
    the player database, using the player ID as the marker.
    """
    # Selects all the players from the database and filter the 
    # player with matching ID
    statement = db.select(Player).where(Player.player_id == player_id)
    player = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = player_schema.dump(player)

    # Return the search results if this player is in the player 
    # database, otherwise inform the user that the player does 
    # not exist.
    if queryData:
        # Return the player info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Player with this ID does not exist
        return error_player_does_not_exist(player_id)
    

@playersBp.route("/<int:player_id>", methods = ["PUT", "PATCH"])
def updatePlayer(player_id):
    """
    Retrieve the body data and update the details of the player 
    with the matching ID in the player database, this is the 
    equivalent of PUT/PATCH in postgresql.
    """
    # Selects all the players from the database and filter the 
    # player with matching ID
    statement = db.select(Player).where(Player.player_id == player_id)
    player = db.session.scalar(statement)

    # Update the player information in the players database if 
    # they exist
    if player:
        # Fetch the player information from the request body
        bodyData = request.get_json()

        # Update the player's details with these new changes, 
        # otherwise reuse the same information
        player.player_name = bodyData.get("player_name", player.player_name)
        
        # Commit and permanently update the player data in the 
        # postgresql database
        db.session.commit()

        # Return the updated player info in JSON format
        return jsonify(player_schema.dump(player))
    else:
        # Return an error message: Player with this ID does not exist
        return error_player_does_not_exist(player_id)
    

@playersBp.route("/<int:player_id>", methods = ["DELETE"])
def deletePlayer(player_id):
    """
    Find the player with the matching ID in the player database 
    and remove them. This is the equivalent of DELETE in postgresql.
    """
    # Selects all the players from the database and filter the player with
    # matching ID
    statement = db.select(Player).where(Player.player_id == player_id)
    player = db.session.scalar(statement)

    # Delete the player from the players database if they exist
    if player:
        # Remove the player from the session
        db.session.delete(player)
        
        # Commit and permanently remove the player data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return player_successfully_removed(player.player_name)
    else:
        # Return an error message: Player with this ID does not exist
        return error_player_does_not_exist(player_id)