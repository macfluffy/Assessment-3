"""
This file defines the model for the 'event' junction table and it's 
relationships with 'organisers' and the 'venues' models. 
"""
# Built-in imports
import enum
from datetime import date

# Local imports
from init import db


"""
Enumerated values for attributes of an event that have a value from a 
pre-defined set
"""

class EventStatus(enum.Enum):
    """
    This defines the activity status of an event.
    """
    Cancelled = "cancelled"
    Completed = "completed"
    Onhold = "onhold"
    Planned = "planned"
    Running = "running"


class Event(db.Model):
    """
    The event table template contains the information about an event
    hosted by an organiser at a venue. Event attributes are:
        - Event ID: Unique identifier of the event
        - Organiser ID: Organiser hosting the event
        - Venue ID: Venue location the event is being held
        - Event Name: Name of the game event
        - Player Cap: Maximum limit of players allowed to attend
        - Event Date: When is the event happening?
        - Event Details: Extra information about the event
        - Event Status: Filter/Validation value to know if the 
                        event is on, cancelled, or planned
    """
    
    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "events"

    # Table columns
    event_id = db.Column(db.Integer, primary_key = True) 
    organiser_id = db.Column(
        db.Integer, 
        db.ForeignKey("organisers.organiser_id")
    )
    venue_id = db.Column(
        db.Integer, 
        db.ForeignKey("venues.venue_id")
    )
    event_name = db.Column(db.String())
    player_cap = db.Column(db.Integer)
    event_date = db.Column(db.Date, default = date.today())
    event_details = db.Column(db.String())
    event_status = db.Column(db.Enum(EventStatus))

    """
    Relationships:
        - Event: An event is hosted by an organiser at a venue.
        - Registration: An event needs registration to attend.
    """
    # Define the relationships between organisers, venues, and events
    organiser = db.relationship("Organiser", back_populates = "events")
    venue = db.relationship("Venue", back_populates = "events")
    # Delete the registration if the event is deleted
    registrations = db.relationship(
        "Registration",
        back_populates = "event",
        cascade = "all, delete"
    )