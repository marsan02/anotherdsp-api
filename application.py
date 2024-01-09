# application.py

from flask import Flask
from main import configure_routes
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure routes
    configure_routes(app)

    return app

app = create_app()  # Rename 'application' to 'app'
if __name__ == '__main__':
    app.run(debug=True)
