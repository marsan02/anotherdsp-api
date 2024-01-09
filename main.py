from flask import Flask, request, jsonify, request, render_template, redirect,url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import utils.geo_api as geo_api
import requests
from utils.auth import requires_auth, handle_auth_error, AuthError
import os
import services.campaign as campaigns
load_dotenv()  # This loads the environment variables from .env



def configure_routes(app):


    # MongoDB Atlas connection URI
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    app.register_error_handler(AuthError, handle_auth_error)

    @app.route('/countries')
    @requires_auth
    def get_countries():
        return geo_api.get_countries()

    @app.route('/submit-campaign', methods=['POST'])
    @requires_auth
    def submit_campaign():
        return campaigns.post_campaign(request,client)

    @app.route('/campaigns', methods=['GET'])
    @requires_auth
    def manage_campaigns():
        return campaigns.list_all_campaigns(client)

    @app.route('/campaigns/<campaign_name>', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_campaign(campaign_name):
        if request.method == 'GET':
            #retrieve campaign
            return campaigns.get_campaign(campaign_name,client)
        elif request.method == 'PUT':
            # Update a campaign
            return campaigns.put_campaign(campaign_name,request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a campaign
            return campaigns.delete_campaign(campaign_name,client)

    # Example of a protected route
    @app.route('/')
    def your_protected_route():
        # Now this route only requires the user to be authenticated
        return 'Welcome to Another DSP API'

if __name__ == '__main__':
    app.run(debug=True)