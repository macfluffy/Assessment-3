"""
This file creates the Create, Read, Update, and Delete operations to 
the registration data, through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.registration import Registration
from schemas.registration_schema import registration_schema, registrations_schema

# Create the Template Web Application Interface for card routes to 
# be applied to the Flask application
registrationsBp = Blueprint(
    "registrations", 
    __name__, 
    url_prefix = "/registrations"
)


"""
Registration Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No records found. Add a statement to get started."
    }, 404

def error_registration_does_not_exist(event_id, player_id):
    return {
        "message": 
        f"Player ID {player_id}'s registration to Event ID {event_id} does not exist."
    }, 404


"""
API Routes
"""

@registrationsBp.route("/", methods = ["POST"])
def create_registration():
    """
    Retrieve the body data and add the details of the registration 
    into the registration database, this is the equivalent of POST 
    in postgresql. This is how players officially signup for events.
    """
    # Fetch the registration information from the request body
    bodyData = request.get_json()

    # Create a new entry into the registration using the request body 
    # data and the registration schema will organise the data to their 
    # matching attributes with validation rules implemented.
    newRegistration = registration_schema.load(
        bodyData,
        session = db.session
    )
   
    # Add the registration data into the session
    db.session.add(newRegistration)
    
    # Commit and write the registration data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(registration_schema.dump(newRegistration)), 201


@registrationsBp.route("/")
def get_registrations():
    """
    Retrieve and read all the registrations from the registrations 
    database, this is the equivalent of GET in postgresql.
    """
    # Select all the registrations from the database and the decks 
    # that players will be using in the event
    event_id = request.args.get("event_id", type = int)
    player_id = request.args.get("player_id", type = int)
    statement = db.select(Registration)
    
    # Display events that exist
    if event_id:
        statement = statement.where(Registration.event_id == event_id)
    
    # Display players that exist in these events
    if player_id:
        statement = statement.where(Registration.player_id == player_id)

    # Serialise it as the scalar result is unserialised
    registrations_list = db.session.scalars(statement)
    queryData = registrations_schema.dump(registrations_list)

    # Return the search results if there are registrations in the 
    # registration database, otherwise inform the user that the 
    # database is empty.
    if queryData:
        # Return the list of registrations in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Registrations table is empty
        return error_empty_table()