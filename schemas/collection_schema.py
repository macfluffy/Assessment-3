# Installed import packages
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields

# Local imports - Collection table template
from models.collection import Collection


class CollectionSchema(SQLAlchemyAutoSchema):
    """
    The collection schema template. This organises the JSON response when 
    fetching collection information such as the decks in a players' 
    collection.
    """
    class Meta:
        model = Collection
        load_instance = True
        include_fk = True

        # Define the exact order of how the JSON query is displayed
        # Player ID, Deck ID
        fields = (
            "collection_id",
            "player_id",
            "players",
            "deck_id",
            "decks"
        )

    # Only show the name of the player when showing player 
    # information in the collection query
    players = fields.Nested(
        "PlayerSchema", 
        only = (
            "player_name",
        )
    )

    # Only show the name of the deck when showing deck information in
    # the collection query
    decks = fields.Nested(
        "DeckSchema", 
        only = (
            "deck_name",
        )
    )

# Create instances of the schema for the controllers to call when 
# applying validation, error handling and restrictions
collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many = True)