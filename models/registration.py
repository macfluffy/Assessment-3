"""
This file defines the model for the 'registration' junction table and it's 
relationships with 'events' and the 'players' models. 
"""
# Built-in imports
from datetime import date

# Local imports
from init import db

class Registration(db.Model):
    """
    The registration table template contains the information about a 
    player's sign in for the event. Registrations cannot exist without 
    a player to attend nor can it exist without an event to be
    attended.
    """
    
    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "registrations"
    
    # Define the primary key as a union of both the event_id and player_id
    __table_args__ = (
        db.PrimaryKeyConstraint(
            "event_id", 
            "player_id", 
            name = "player_registration"
        ),
    )

    # Table columns
    event_id = db.Column(
        db.Integer, 
        db.ForeignKey("events.event_id"), 
        nullable = False
    )
    player_id = db.Column(
        db.Integer, 
        db.ForeignKey("players.player_id"), 
        nullable = False
    )
    # nullable as players can register before they add their deck
    registered_deck = db.Column(
        db.Integer,
        db.ForeignKey("collections.collection_id")
    )
    registration_date = db.Column(db.Date, default = date.today())

    # Define the relationships between events, players, and registrations
    event = db.relationship("Event", back_populates = "registrations")
    player = db.relationship("Player", back_populates = "registrations")