"""
This file defines the model for the 'ranking' junction table and it's 
relationships with 'events' and the 'players' models. 
"""
# Local imports
from init import db

class Ranking(db.Model):
    """
    The ranking table template contains the information about a 
    player's performance in an event. Rankings cannot exist without 
    a player playing at an event.
    """
    
    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "rankings"
    
    # Table columns
    player_id = db.Column(
        db.Integer, 
        db.ForeignKey("players.player_id"), 
        nullable = False
    )
    event_id = db.Column(
        db.Integer, 
        db.ForeignKey("events.event_id"), 
        nullable = False
    )
    placement = db.Column(db.Integer)
    points = db.Column(db.Integer, default = 0)
    wins = db.Column(db.Integer, default = 0)
    losses = db.Column(db.Integer, default = 0)
    ties = db.Column(db.Integer, default = 0)

    # Define the primary key as a union of both the event_id and player_id
    # Primary key means player & event combination uniqueness and cannot 
    # be nulled.
    __table_args__ = (
        db.PrimaryKeyConstraint(
            "player_id", 
            "event_id", 
            name = "player_ranking"
        ),
    )

    # Define the relationships between events, players, and rankings
    player = db.relationship("Player", back_populates = "rankings")
    event = db.relationship("Event", back_populates = "rankings")