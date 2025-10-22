"""
This file creates the structure on how organiser data should be organised 
within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp
from marshmallow import fields

# Local imports - Organiser table template
from models.organiser import Organiser


class OrganiserSchema(SQLAlchemyAutoSchema):
    """
    The organiser schema template. This organises the JSON response when 
    fetching organiser information such as the organiser's name, and 
    contact details.
    """
    class Meta:
        model = Organiser
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Organiserer Name, Email, and Phone Number
        fields = (
            "organiser_id", 
            "organiser_name",
            "organiser_email",
            "organiser_number"
        )

    # An organiser cannot have a blank name
    organiser_name = auto_field(
        validate = [
            Length(
                min = 1,
                error = "An organiser needs a name and it cannot be blank."
            ),
            Regexp(
                r"[^\s]",
                error = "An organiser's name cannot start with a blank."
            )
        ]
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
organiser_schema = OrganiserSchema()
organisers_schema = OrganiserSchema(many = True)