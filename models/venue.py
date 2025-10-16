"""
This file defines the model for the 'venues' table and it's relationships. 
"""
# Local imports
from init import db

class Venue(db.Model):
    """
    The deck table template. This contains the name of a venue, their 
    contact details, location and the relationships between the venue and
    the events held at their location.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "venues"

    # Table columns
    venue_id = db.Column(db.Integer, primary_key = True)
    venue_name = db.Column(db.String(), nullable = False)
    venue_address = db.Column(db.String())
    venue_number = db.Column(db.String())

    """
    Define the special relationships:
      - Event: An event is held at a venue/location.
    """
    # Null this in the events, when deleted. The event still occured, 
    # and kept in the database for records.
    events = db.relationship(
        "Event",
        back_populates = "venue",
        cascade = "all, delete"
    )