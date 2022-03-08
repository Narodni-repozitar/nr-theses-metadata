from flask import Blueprint


def create_blueprint_from_app(app):
    """Create  blueprint."""
    return app.extensions["nr_theses_metadata"].resource.as_blueprint()


static_blueprint = Blueprint(
    '__static_to_be_moved__',
    __name__,
    static_folder='static',
)
