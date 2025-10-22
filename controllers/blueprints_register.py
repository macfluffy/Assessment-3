"""
This file applies all the route controllers to the flask application
when called.
"""
# Local imports - Blueprint route controllers
from controllers.cli_controller import dbCommands
from controllers.card_controller import cardsBp
from controllers.deck_controller import decksBp
from controllers.player_controller import playersBp
from controllers.organiser_controller import organisersBp
from controllers.venue_controller import venuesBp
from controllers.decklist_controller import decklistsBp
from controllers.collection_controller import collectionsBp
from controllers.event_controller import eventsBp
from controllers.registration_controller import registrationsBp
from controllers.ranking_controller import rankingsBp

def attach_blueprints(app):
    """
    Apply the imported routes created in the controllers folder to this 
    instance of Flask app
    """
    app.register_blueprint(dbCommands)
    app.register_blueprint(cardsBp)
    app.register_blueprint(decksBp)
    app.register_blueprint(playersBp)
    app.register_blueprint(organisersBp)
    app.register_blueprint(venuesBp)
    app.register_blueprint(decklistsBp)
    app.register_blueprint(collectionsBp)
    app.register_blueprint(eventsBp)
    app.register_blueprint(registrationsBp)
    app.register_blueprint(rankingsBp)