"""
This file creates the structure on how event data should be organised 
within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import OneOf
from marshmallow import fields

# Local imports - Event table template
from models.event import Event, EventStatus


class EventSchema(SQLAlchemyAutoSchema):
    """
    The event schema template. This organises the JSON response when 
    fetching event information such as the organiser, venue, details
    about the event, and the player caps.
    """
    class Meta:
        model = Event
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Event ID, Organiser ID, Venue ID, Event Details
        fields = (
            "event_id",
            "organiser_id",
            "organiser",
            "venue_id",
            "venue",
            "event_name",
            "player_cap",
            "event_date",
            "event_details",
            "event_status"
        )

    # Only show the name of the organiser when showing organiser 
    # information in the event query
    organiser = fields.Nested(
        "OrganiserSchema", 
        only = [
            "organiser_name",
        ]
    )

    # Only show the name of the venue when showing venue information in
    # the event query
    venue = fields.Nested(
        "VenueSchema", 
        only = [
            "venue_name",
        ]
    )

    # Only acceptable values are
    event_status = auto_field(
        validate = OneOf(
            [
                EventStatus.Cancelled,
                EventStatus.Completed,
                EventStatus.Onhold,
                EventStatus.Planned,
                EventStatus.Running
            ],
            error = "Only valid statuses are allowed. Cancelled, Completed, Onhold, Planned, or Running."
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
event_schema = EventSchema()
events_schema = EventSchema(many = True)