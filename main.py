from flask import Flask, request, jsonify, request, render_template, redirect,url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import utils.geo_api as geo_api
import requests
from utils.auth import requires_auth, handle_auth_error, AuthError
import os
import services.campaign as campaigns
import services.creative as creatives
import services.advertiser as advertisers
import services.deal as deals
import services.buyer as buyers
import services.seller as sellers

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

    @app.route('/submit-campaign', methods=['POST','PUT'])
    @requires_auth
    def submit_campaign():
        if request.method == 'POST':
            #retrieve campaign
            return campaigns.post_campaign(request,client)
        elif request.method == 'PUT':
            # Update a campaign
            campaign_id=request.args.get('_id')
            return campaigns.put_campaign(campaign_id,request,client)
    @app.route('/campaigns', methods=['GET'])
    @requires_auth
    def manage_campaigns():
        return campaigns.list_all_campaigns(client,request.args)

    @app.route('/campaign', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_campaign():
        if request.method == 'GET':
            #retrieve campaign
            return campaigns.get_campaign(request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a campaign
            return campaigns.put_campaign(request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a campaign
            return campaigns.delete_campaign(campaign_name,client)

    @app.route('/submit-creative', methods=['POST'])
    @requires_auth
    def submit_creative():
        return creatives.post_creative(request,client)

    @app.route('/creatives', methods=['GET'])
    @requires_auth
    def manage_creatives():
        return creatives.get_creative(client,request.args)

    @app.route('/creatives/<creative_name>', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_creative(creative_name):
        if request.method == 'GET':
            #retrieve creative
            return creatives.get_creative(creative_name,client)
        elif request.method == 'PUT':
            # Update a creative
            return creatives.put_creative(creative_name,request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a creative
            return creative.delete_creative(creative_name,client)
    
    @app.route('/submit-advertiser', methods=['POST','PUT'])
    @requires_auth
    def submit_advertiser(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            #retrieve advertiser
            return advertisers.post_advertiser(buyer_id,request,client)
        elif request.method == 'PUT':
            # Update a advertiser
            advertiser_id=request.args.get('_id')
            return advertisers.put_advertiser(buyer_id,advertiser_id,request,client)
    @app.route('/advertisers', methods=['GET'])
    @requires_auth
    def manage_advertiser():
        return advertisers.list_all_advertisers(client)

    @app.route('/advertiser', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_advertiser():
        if request.method == 'GET':
            #retrieve advertiser
            return advertisers.get_advertiser(request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a advertiser
            return advertisers.put_advertisers(request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a advertiser
            return advertisers.delete_advertiser(advertiser_name,client)

    @app.route('/submit-buyer', methods=['POST','PUT'])
    @requires_auth
    def submit_buyer():
        if request.method == 'POST':
            #retrieve buyer
            return buyers.post_buyer(request,client)
        elif request.method == 'PUT':
            # Update a buyer
            buyer_id=request.args.get('_id')
            return buyers.put_buyer(buyer_id,request,client)
    @app.route('/buyers', methods=['GET'])
    @requires_auth
    def manage_buyer():
        return buyers.list_all_buyers(client)

    @app.route('/buyer', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_buyer():
        if request.method == 'GET':
            #retrieve buyer
            return buyers.get_buyer(request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a buyer
            return buyers.put_buyer(request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a buyer
            return buyers.delete_buyer(buyer_name,client)

    @app.route('/submit-deal', methods=['POST','PUT'])
    @requires_auth
    def submit_deal():
        if request.method == 'POST':
            #retrieve deal
            return deals.post_deal(request,client)
        elif request.method == 'PUT':
            # Update a deal
            deal_id=request.args.get('_id')
            return deals.put_deal(deal_id,request,client)
    @app.route('/deals', methods=['GET'])
    @requires_auth
    def manage_deal():
        return deals.list_all_deals(client)

    @app.route('/deal', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_deal():
        if request.method == 'GET':
            #retrieve deal
            return deals.get_deal(request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a deal
            return deals.put_deal(request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a deal
            return deals.delete_deal(deal_name,client)


    @app.route('/submit-seller', methods=['POST','PUT'])
    @requires_auth
    def submit_seller():
        if request.method == 'POST':
            #retrieve seller
            return sellers.post_seller(request,client)
        elif request.method == 'PUT':
            # Update a seller
            seller_id=request.args.get('_id')
            return sellers.put_seller(seller_id,request,client)
    @app.route('/sellers', methods=['GET'])
    @requires_auth
    def manage_seller():
        return sellers.list_all_sellers(client)

    @app.route('/seller', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_seller():
        if request.method == 'GET':
            #retrieve seller
            return sellers.get_seller(request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a seller
            return sellers.put_seller(request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a seller
            return sellers.delete_seller(seller_name,client)





    # Example of a protected route
    @app.route('/')
    def your_protected_route():
        # Now this route only requires the user to be authenticated
        return 'Welcome to Another DSP API'

if __name__ == '__main__':
    app.run(debug=True)