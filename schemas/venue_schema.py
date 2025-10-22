"""
This file creates the structure on how venue data should be organised 
within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp
from marshmallow import fields

# Local imports - Venue table template
from models.venue import Venue

class VenueSchema(SQLAlchemyAutoSchema):
    """
    The venue schema template. This organises the JSON response when 
    fetching venue information such as the venue's name, location 
    and contact details.
    """
    class Meta:
        model = Venue
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Venue Name, Address, and Phone Number
        fields = (
            "venue_id", 
            "venue_name",
            "venue_address",
            "venue_number"
        )

    # A venue's name cannot be blank
    venue_name = auto_field(
        validate = [
            Length(
                min = 1,
                error = "A venue needs a name and it cannot be blank."
            ),
            Regexp(
                r"[^\s]",
                error = "A venue's name cannot start with a blank."
            )
        ]
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
venue_schema = VenueSchema()
venues_schema = VenueSchema(many = True)
