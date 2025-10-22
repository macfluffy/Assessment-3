"""
This file creates the Create, Read, Update, and Delete operations 
to the event data, through REST API design using Flask 
Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.event import Event
from schemas.event_schema import event_schema, events_schema
# from schemas.schemas import event_schema, events_schema

# Create the Template Web Application Interface for card routes 
# to be applied to the Flask application
eventsBp = Blueprint("events", __name__, url_prefix = "/events")


"""
Event Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No records found. Add a statement to get started."
    }, 404

def error_event_does_not_exist(event_id):
    return {
        "message": 
        f"Event ID {event_id} does not exist in this table."
    }, 404

def event_sucessfully_deleted(event_id):
    return {
        "message": 
        f"Event ID {event_id} has been removed."
    }, 200 


"""
API Routes
"""

@eventsBp.route("/", methods = ["POST"])
def create_event():
    """
    Retrieve the body data and add the details of the event 
    into the event database, this is the equivalent of POST 
    in postgresql.
    """
    # Fetch the event information from the request body
    bodyData = request.get_json()

    # Create a new entry into the event using the request body data 
    # and the event schema will organise the data to their 
    # matching attributes with validation rules implemented.
    newEvent = event_schema.load(
        bodyData,
        session = db.session
    )
    # newEvent = Event(
    #     organiser_id = bodyData.get("organiser_id"),
    #     venue_id = bodyData.get("venue_id"),
    #     event_name = bodyData.get("event_name"),
    #     player_cap = bodyData.get("player_cap"),
    #     event_date = bodyData.get("event_date"),
    #     event_details = bodyData.get("event_details"),
    #     event_status = bodyData.get("event_status")
    # )
    
    # Add the event data into the session
    db.session.add(newEvent)
    
    # Commit and write the event data from this session into 
    # the postgresql database
    db.session.commit()
    return jsonify(event_schema.dump(newEvent)), 201


@eventsBp.route("/")
def get_events():
    """
    Retrieve and read all the events from the events 
    database, this is the equivalent of GET in postgresql.
    """
    # Select all the events from the database
    event_id = request.args.get("event_id", type = int)
    organiser_id = request.args.get("organiser_id", type = int)
    venue_id = request.args.get("venue_id", type = int)
    statement = db.select(Event)
    
    # Display events that exist
    if event_id:
        statement = statement.where(Event.event_id == event_id)

    # Display organisers that host this event
    if organiser_id:
        statement = statement.where(Event.organiser_id == organiser_id)
    
    # Display venues that exist in the filtered event
    if venue_id:
        statement = statement.where(Event.venue_id == venue_id)

    # Serialise it as the scalar result is unserialised
    events_list = db.session.scalars(statement)
    queryData = events_schema.dump(events_list)

    # Return the search results if there are events in the 
    # event database, otherwise inform the user that the 
    # database is empty.
    if queryData:
        # Return the list of events in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Events table is empty
        return error_empty_table()
    

@eventsBp.route("/<int:event_id>", methods = ["DELETE"])
def delete_event(event_id):
    """
    Find the event with the matching ID and remove it from 
    the events database. This is the equivalent of DELETE 
    in postgresql.
    """
    # Selects all the events from the database and filter for 
    # the deck with matching ID
    statement = db.select(Event).where(Event.event_id == event_id)
    
    # Serialise it as the scalar result is unserialised
    event = db.session.scalar(statement)
    queryData = event_schema.dump(event)

    # Delete the event from the events database if they exist
    if queryData:
        # Remove the event from the session
        db.session.delete(event)
        
        # Commit and permanently remove the event data from 
        # the postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return event_sucessfully_deleted(event_id)
    else:
        # Return an error message: Event with this ID does 
        # not exist
        return error_event_does_not_exist(event_id)