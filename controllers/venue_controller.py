"""
This file creates the Create, Read, Update, and Delete operations 
to our venue data, through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.venue import Venue
from schemas.venue_schema import venue_schema, venues_schema

# Create the Template Web Application Interface for venue routes to 
# be applied to the Flask application
venuesBp = Blueprint("venues", __name__, url_prefix = "/venues")


"""
Venue Controller Messages
"""

def error_empty_table():
    return {
        "message": 
        "No venues found in this database. Add a venue to get started."
    }

def error_venue_does_not_exist(venue_id):
    return {
        "message": 
        f"Venue ID {venue_id} does not exist"
    }, 404

def venue_successfully_removed(venue_name):
    return {
        "message": 
        f"The {venue_name} venue has been deleted successfully."
    }, 200 


"""
API Routes
"""

@venuesBp.route("/", methods = ["POST"])
def createVenue():
    """
    Retrieve the body data and add the details of the venue into 
    the venue database, this is the equivalent of POST in 
    postgresql.
    """
    # Fetch the venue information from the request body
    bodyData = request.get_json()
    
    # Create a new venue object with the request body data as 
    # the attributes
    newVenue = venue_schema.load(
        bodyData,
        session = db.session
    )

    # Add the venue data into the session
    db.session.add(newVenue)
    
    # Commit and write the venue data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = venue_schema.dump(newVenue)
    return jsonify(acknowledgement), 201


@venuesBp.route("/")
def getVenues():
    """
    Retrieve and read all the venues from the venue database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the venues from the database
    statement = db.select(Venue)
    venuesList = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = venues_schema.dump(venuesList)
    
    # Return the search results if there are venues in the venue 
    # database, otherwise inform the user that the database is 
    # empty.
    if queryData:
        # Return the list of venues in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Venue table is empty
        return error_empty_table()
    

@venuesBp.route("/<int:venue_id>")
def getVenue(venue_id):
    """
    Retrieve and read a specific venue's information from 
    the venue database, using the venue ID as the marker.
    """
    # Selects all the venues from the database and filter the venue 
    # with matching ID
    statement = db.select(Venue).where(Venue.venue_id == venue_id)
    venue = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = venue_schema.dump(venue)

    # Return the search results if this venue is in the venue 
    # database, otherwise inform the user that the venue does not 
    # exist.
    if queryData:
        # Return the venue info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Venue with this ID does not 
        # exist
        return error_venue_does_not_exist(venue_id)
    

@venuesBp.route("/<int:venue_id>", methods = ["PUT", "PATCH"])
def updateVenue(venue_id):
    """
    Retrieve the body data and update the details of the venue 
    with the matching ID in the venue database, this is the 
    equivalent of PUT/PATCH in postgresql.
    """
    # Selects all the venues from the database and filter the 
    # venue with matching ID
    statement = db.select(Venue).where(Venue.venue_id == venue_id)
    venue = db.session.scalar(statement)

    # Update the venue information in the venues database if 
    # they exist
    if venue:
        # Fetch the venue information from the request body
        bodyData = request.get_json()

        # Update the venue's details with these new changes, 
        # otherwise reuse the same information
        venue.venue_name = bodyData.get(
            "venue_name", 
            venue.venue_name
        )
        venue.venue_address = bodyData.get(
            "venue_address", 
            venue.venue_address
        )
        venue.venue_number = bodyData.get(
            "venue_number", 
            venue.venue_number
        )
        
        # Commit and permanently update the venue data in the 
        # postgresql database
        db.session.commit()

        # Return the updated venue info in JSON format
        return jsonify(venue_schema.dump(venue))
    else:
        # Return an error message: Venue with this ID does not 
        # exist
        return error_venue_does_not_exist(venue_id)
    

@venuesBp.route("/<int:venue_id>", methods = ["DELETE"])
def deleteVenue(venue_id):
    """
    Find the venue with the matching ID in the venue database 
    and remove them. This is the equivalent of DELETE in 
    postgresql.
    """
    # Selects all the venues from the database and filter the 
    # venue with matching ID
    statement = db.select(Venue).where(Venue.venue_id == venue_id)
    venue = db.session.scalar(statement)

    # Delete the venue from the venues database if they exist
    if venue:
        # Remove the venue from the session
        db.session.delete(venue)
        
        # Commit and permanently remove the venue data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return venue_successfully_removed(venue.venue_name)
    else:
        # Return an error message: Venue with this ID does 
        # not exist
        return error_venue_does_not_exist(venue_id)