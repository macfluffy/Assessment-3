"""
This file creates the Create, Read, Update, and Delete operations 
to the ranking data, through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.ranking import Ranking
from schemas.ranking_schema import ranking_schema, rankings_schema

# Create the Template Web Application Interface for card routes 
# to be applied to the Flask application
rankingsBp = Blueprint(
    "rankings", 
    __name__, 
    url_prefix = "/rankings"
)


"""
Ranking Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No records found. Add a statement to get started."
    }, 404

def error_ranking_does_not_exist(event_id, player_id):
    return {
        "message": 
        f"Player ID {player_id} does not have a ranking at Event ID {event_id}."
    }, 404


"""
API Routes
"""

@rankingsBp.route("/", methods = ["POST"])
def create_ranking():
    """
    Retrieve the body data and add the details of the ranking 
    into the ranking database, this is the equivalent of POST 
    in postgresql. This is how players officially signup for 
    events.
    """
    # Fetch the ranking information from the request body
    bodyData = request.get_json()

    # Create a new entry into the ranking using the request body 
    # data and the ranking schema will organise the data to their 
    # matching attributes with validation rules implemented.
    newRanking = ranking_schema.load(
        bodyData,
        session = db.session
    )
   
    # Add the ranking data into the session
    db.session.add(newRanking)
    
    # Commit and write the ranking data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(ranking_schema.dump(newRanking)), 201


@rankingsBp.route("/")
def get_rankings():
    """
    Retrieve and read all the rankings from the rankings 
    database, this is the equivalent of GET in postgresql.
    """
    # Select all the rankings from the database and the decks 
    # that players will be using in the event
    player_id = request.args.get("player_id", type = int)
    event_id = request.args.get("event_id", type = int)
    statement = db.select(Ranking)
    
    # Display players that exist
    if player_id:
        statement = statement.where(Ranking.player_id == player_id)
    
    # Display events that players are attending
    if event_id:
        statement = statement.where(Ranking.event_id == event_id)

    # Serialise it as the scalar result is unserialised
    rankings_list = db.session.scalars(statement)
    queryData = rankings_schema.dump(rankings_list)

    # Return the search results if there are rankings in the 
    # ranking database, otherwise inform the user that the 
    # database is empty.
    if queryData:
        # Return the list of rankings in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Rankings table is empty
        return error_empty_table()