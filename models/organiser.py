"""
This file defines the model for the 'organisers' table and it's relationships. 
"""
# Local imports
from init import db

class Organiser(db.Model):
    """
    The deck table template. This contains the name of a organiser, their 
    contact details and the relationships between the organiser and the 
    events they host.
    """

    # Name of the table and what is referenced by Flask-SQLAlchemy methods
    __tablename__ = "organisers"

    # Table columns
    organiser_id = db.Column(db.Integer, primary_key = True)
    organiser_name = db.Column(db.String(), nullable = False)
    organiser_email = db.Column(db.String())
    organiser_number = db.Column(db.String())