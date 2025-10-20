"""
This file is a template of all the commonly occuring errors when users 
input something that would cause the API to crash, from violating the 
constraints in the schema or the expected data types of the models to 
meeting the data types but failing the validation barriers placed in 
the schemas. This function also reports the errors in a legible manner 
to narrow down where failures occur.
"""

# Imported libraries - For referencing standardised error codes and
# adding elegant error handling to prevent system crashes.
from flask import jsonify # Formats error messages as a JSON
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
from psycopg2 import errorcodes


def register_error_handlers(app):
    """
    This function will attach the error handling functions to the flask 
    app when called in the app file containing the flask app creation 
    function.
    """
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        """
        This function throws a validation error message whenever a user 
        inputs a value that fails to meet the validation/authentication 
        requirements placed on the models in their respective schemas.
        """
        return jsonify(err.messages), 404
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        """
        This function throws an integrity error message whenever a 
        user inputs a value that defies the table column constraints as
        defined in the models and their schemas.
        """
        if hasattr(err, "orig") and err.orig:
            # Throw error code 23502: Not Null Violation when a user 
            # enters a null value to an attribute with a not null 
            # constraint
            if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
                return {
                    "message": 
                    f"Required field: {err.orig.diag.column_name} cannot be null."
                }, 409
            
            # Throw a unique violation message if a user enters a value 
            # that matches one already existing in this column in the 
            # respective table
            if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
                return {
                    "message": 
                    err.orig.diag.message_detail
                }, 409
            
            # Throw a foreign key violation message if a user enters a 
            # value in place of the foreign keys that does not exist 
            # in its primary table
            if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                return {
                    "message": 
                    err.orig.diag.message_detail
                }, 409
            
            # Check violation code 23514: Notify the user if they 
            # entered a value that does not satisfy the constraint 
            # placed on the column
            if err.orig.pgcode == errorcodes.CHECK_VIOLATION:
                return {
                    "message": 
                    f"[23514] Check Violation: A value that doesn't satisfy a column's constraints has been entered; {err.orig.diag.message_detail}"
                }, 409
            
            # Throw a generic integrity error message, if a user has 
            # entered an erroneous value that falls under the integrity 
            # error but is not defined by the common error codes   
            else:
                return {
                    "message": 
                    "Unknown integrity error occured."
                }, 409
        
        # # Throw a generic integrity error message, if a user has 
        # entered an erroneous value that falls under the integrity 
        # error but there is no error code 
        else:
            return  {
                "message": 
                "Integrity Error occured."
            }, 409
        
    @app.errorhandler(DataError)
    def handle_data_error(err):
        """
        This function throws a data error message whenever a user 
        inputs a value out of range in that column.
        """
        return {
            "message": 
            f"{err.orig.diag.message_primary}"
        }, 409
    
    @app.errorhandler(404)
    def handle_404(err):
        """
        This function throws a 404 error message when the page or 
        route cannot be found.
        """
        return {
            "message": 
            "Requested resource not found/ does not exist"
        }, 404
    
    @app.errorhandler(500)
    def handle_server_related_error(err):
        """
        This function throws a 500 error message when there is 
        something wrong on the server side. This may not return an 
        error message if the server itself is down.
        """
        return {
            "message": 
            "Server error occured. Please contact the site administration."
        }, 500