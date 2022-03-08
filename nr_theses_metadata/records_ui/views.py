def create_ui_blueprint(app):
    """Create  blueprint."""
    return app.extensions["nr_theses_metadata"].records_ui_resource.as_blueprint()
