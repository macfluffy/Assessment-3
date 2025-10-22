"""
This file creates the structure on how player data should be organised 
within our relational database, their constraints, and the 
relationships between each of these tables.
"""

# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow.validate import Length, Regexp
from marshmallow import fields

# Local imports - Player table template
from models.player import Player


class PlayerSchema(SQLAlchemyAutoSchema):
    """
    The player schema template. This organises the JSON response when 
    fetching player information such as the player's name.
    """
    class Meta:
        model = Player
        load_instance = True

        # Define the exact order of how the JSON query is displayed
        # Player Name
        fields = (
            "player_id", 
            "player_name"
        )

    # Player's must not be blank
    player_name = auto_field(
        validate = [
            Length(
                min = 1,
                error = "A player needs a name and it cannot be blank."
            ),
            Regexp(
                r"[^\s]",
                error = "A player's name cannot start with a blank."
            )
        ]
    )


# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
player_schema = PlayerSchema()
players_schema = PlayerSchema(many = True)