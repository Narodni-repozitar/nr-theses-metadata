def create_blueprint_from_app(app):
    """Create  blueprint."""
    return app.extensions["nr_theses_metadata"].resource.as_blueprint()


def create_ui_blueprint_from_app(app):
    """Create  blueprint."""
    return app.extensions["nr_theses_metadata"].ui_resource.as_blueprint()
