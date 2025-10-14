"""
This file creates the Create, Read, Update, and Delete operations to our organiser data,
through REST API design using Flask Blueprint.
"""

# Installed import packages
from flask import Blueprint, jsonify, request

# Local imports
from init import db
from models.organiser import Organiser
from schemas.schemas import organiser_schema, organisers_schema

# Create the Template Web Application Interface for organiser routes to be applied 
# to the Flask application
organisersBp = Blueprint("organisers", __name__, url_prefix = "/organisers")


"""
Organiser Controller Messages
"""

def error_empty_table():
    return {"message": "No organisers found in this database. Add a organiser to get started."}

def error_organiser_does_not_exist(organiser_id):
    return {"message": f"Organiser ID {organiser_id} does not exist"}, 404

def organiser_successfully_removed(organiser_name):
    return {"message": f"Organiser {organiser_name} deleted successfully."}, 200 


"""
API Routes
"""

@organisersBp.route("/", methods = ["POST"])
def createOrganiser():
    """
    Retrieve the body data and add the details of the organiser into the organiser database,
    this is the equivalent of POST in postgresql.
    """
    # Fetch the organiser information from the request body
    bodyData = request.get_json()
    
    # Create a new organiser object with the request body data as the attributes
    newOrganiser = Organiser(
        organiser_name = bodyData.get("organiser_name"),
        organiser_email = bodyData.get("organiser_email"),
        organiser_number = bodyData.get("organiser_number")
    )

    # Add the organiser data into the session
    db.session.add(newOrganiser)
    
    # Commit and write the organiser data from this session into 
    # the postgresql database
    db.session.commit()

    # Send acknowledgement
    acknowledgement = organiser_schema.dump(newOrganiser)
    return jsonify(acknowledgement), 201


@organisersBp.route("/")
def getOrganisers():
    """
    Retrieve and read all the organisers from the organiser database,
    this is the equivalent of GET in postgresql.
    """
    # Selects all the organisers from the database
    statement = db.select(Organiser)
    organisersList = db.session.scalars(statement)

    # Serialise it as the scalar result is unserialised
    queryData = organisers_schema.dump(organisersList)
    
    # Return the search results if there are organisers in the organiser database, 
    # otherwise inform the user that the database is empty.
    if queryData:
        # Return the list of organisers in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Organiser table is empty
        return error_empty_table()
    

@organisersBp.route("/<int:organiser_id>")
def getOrganiser(organiser_id):
    """
    Retrieve and read a specific organiser's information from 
    the organiser database, using the organiser ID as the marker.
    """
    # Selects all the organisers from the database and filter the organiser with
    # matching ID
    statement = db.select(Organiser).where(Organiser.organiser_id == organiser_id)
    organiser = db.session.scalar(statement)

    # Serialise it as the scalar result is unserialised
    queryData = organiser_schema.dump(organiser)

    # Return the search results if this organiser is in the organiser database, 
    # otherwise inform the user that the organiser does not exist.
    if queryData:
        # Return the organiser info in JSON format
        return jsonify(queryData)
    else:
        # Return an error message: Organiser with this ID does not exist
        return error_organiser_does_not_exist(organiser_id)
    

@organisersBp.route("/<int:organiser_id>", methods = ["PUT", "PATCH"])
def updateOrganiser(organiser_id):
    """
    Retrieve the body data and update the details of the organiser with the 
    matching ID in the organiser database, this is the equivalent of 
    PUT/PATCH in postgresql.
    """
    # Selects all the organisers from the database and filter the organiser with
    # matching ID
    statement = db.select(Organiser).where(Organiser.organiser_id == organiser_id)
    organiser = db.session.scalar(statement)

    # Update the organiser information in the organisers database if they exist
    if organiser:
        # Fetch the organiser information from the request body
        bodyData = request.get_json()

        # Update the organiser's details with these new changes, otherwise 
        # reuse the same information
        organiser.organiser_name = bodyData.get("organiser_name", organiser.organiser_name)
        organiser.organiser_email = bodyData.get("organiser_email", organiser.organiser_email)
        organiser.organiser_number = bodyData.get("organiser_number", organiser.organiser_number)
        
        # Commit and permanently update the organiser data in the 
        # postgresql database
        db.session.commit()

        # Return the updated organiser info in JSON format
        return jsonify(organiser_schema.dump(organiser))
    else:
        # Return an error message: Organiser with this ID does not exist
        return error_organiser_does_not_exist(organiser_id)
    

@organisersBp.route("/<int:organiser_id>", methods = ["DELETE"])
def deleteOrganiser(organiser_id):
    """
    Find the organiser with the matching ID in the organiser database and remove them.
    This is the equivalent of DELETE in postgresql.
    """
    # Selects all the organisers from the database and filter the organiser with
    # matching ID
    statement = db.select(Organiser).where(Organiser.organiser_id == organiser_id)
    organiser = db.session.scalar(statement)

    # Delete the organiser from the organisers database if they exist
    if organiser:
        # Remove the organiser from the session
        db.session.delete(organiser)
        
        # Commit and permanently remove the organiser data from the 
        # postgresql database
        db.session.commit()
        
        # Return an acknowledgement
        return organiser_successfully_removed(organiser.organiser_name)
    else:
        # Return an error message: Organiser with this ID does not exist
        return error_organiser_does_not_exist(organiser_id)