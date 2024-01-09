# application.py

from flask import Flask
from utils.logger import setup_logging
from services.campaign_selection_service import load_campaigns_into_cache 
from bidbus.routes import configure_routes

def create_app():
    app = Flask(__name__)

    # Load campaigns into cache
    with app.app_context():
        load_campaigns_into_cache()

    # Setup logging
    setup_logging()

    # Configure routes
    configure_routes(app)

    return app

app = create_app()  # Rename 'application' to 'app'
