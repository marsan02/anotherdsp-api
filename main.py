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
import services.reporting as reporting

load_dotenv()  # This loads the environment variables from .env



def configure_routes(app):


    # MongoDB Atlas connection URI
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    app.register_error_handler(AuthError, handle_auth_error)

    @app.route('/countries')
    @requires_auth
    def get_countries(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return geo_api.get_countries()

    @app.route('/submit-campaign', methods=['POST','PUT'])
    @requires_auth
    def submit_campaign(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            #retrieve campaign
            return campaigns.post_campaign(buyer_id,request,client)
        elif request.method == 'PUT':
            # Update a campaign
            campaign_id=request.args.get('_id')
            return campaigns.put_campaign(buyer_id,campaign_id,request,client)
    @app.route('/campaigns', methods=['GET'])
    @requires_auth
    def manage_campaigns(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return campaigns.list_all_campaigns(buyer_id,client,request.args)

    @app.route('/campaign', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_campaign(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve campaign
            return campaigns.get_campaign(buyer_id,request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a campaign
            return campaigns.put_campaign(buyer_id,request.args['_id'],request,client)
    
        elif request.method == 'DELETE':
            # Delete a campaign
            return campaigns.delete_campaign(buyer_id,request.args['_id'],client)

    @app.route('/submit-creative', methods=['POST','PUT'])
    @requires_auth
    def submit_creative(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method =='POST':
            return creatives.post_creative(buyer_id,request,client)
        elif request.method == 'PUT':
            return creatives.put_creative(buyer_id,request.args['_id'],request,client)
         

    @app.route('/creatives', methods=['GET'])
    @requires_auth
    def manage_creatives(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return creatives.list_all_creatives(buyer_id,client,request.args)

    @app.route('/creative', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_creative(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve creative
            return creatives.get_creative(buyer_id,client,request.args)
        elif request.method == 'PUT':
            # Update a creative
            return creatives.put_creative(buyer_id,request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a creative
            return creatives.delete_creative(buyer_id,request.args['_id'],client)
    
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
    def manage_advertiser(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return advertisers.list_all_advertisers(buyer_id,client)

    @app.route('/advertiser', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_advertiser(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve advertiser
            return advertisers.get_advertiser(buyer_id,request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a advertiser
            return advertisers.put_advertisers(buyer_id,request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a advertiser
            return advertisers.delete_advertiser(buyer_id,request.args['_id'],client)

    @app.route('/submit-buyer', methods=['POST','PUT'])
    @requires_auth
    def submit_buyer(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            #retrieve buyer
            return buyers.post_buyer(buyer_id,request,client)
        elif request.method == 'PUT':
            # Update a buyer
            buyer_id=request.args.get('_id')
            return buyers.put_buyer(buyer_id,request,client)
    @app.route('/buyers', methods=['GET'])
    @requires_auth
    def manage_buyer(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return buyers.list_all_buyers(buyer_id,client)

    @app.route('/buyer', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_buyer(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve buyer
            return buyers.get_buyer(buyer_id,request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a buyer
            return buyers.put_buyer(buyer_id,request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a buyer
            return buyers.delete_buyer(buyer_id,buyer_name,client)

    @app.route('/submit-deal', methods=['POST','PUT'])
    @requires_auth
    def submit_deal(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            #retrieve deal
            return deals.post_deal(buyer_id,request,client)
        elif request.method == 'PUT':
            # Update a deal
            deal_id=request.args.get('_id')
            return deals.put_deal(buyer_id,deal_id,request,client)


    @app.route('/reporting', methods=['POST'])
    @requires_auth
    def submit_report(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            payload = request.json
            return reporting.run_report(buyer_id,payload['dimensions'],payload['metrics'],payload['filters'])

    @app.route('/campaign-monitoring', methods=['GET'])
    @requires_auth
    def process_campaign_monitoring(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        buyer_id = kwargs.get('buyer_id', None)
        all_campaigns = campaigns.list_all_campaigns(buyer_id,client,request.args)
        payload = {"dimensions":["campaign_id"],"metrics":["bids","imps","clicks","viewable_imps","spend","revenue"],"filters":[]}
        reporting_data = reporting.run_report(buyer_id,payload['dimensions'],payload['metrics'],payload['filters'])
        campaign_lookup = {campaign['_id']: campaign for campaign in all_campaigns}
        stitched_data = []
        print(reporting_data)
        for report in reporting_data:
            print(report)
            campaign_id = report['campaign_id']
            if campaign_id in campaign_lookup:
                # Merge the dictionaries (Python 3.5+)
                merged = {**campaign_lookup[campaign_id], **report}
                stitched_data.append(merged)
        return stitched_data


    @app.route('/deals', methods=['GET'])
    @requires_auth
    def manage_deal(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return deals.list_all_deals(buyer_id,client)

    @app.route('/deal', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_deal(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve deal
            return deals.get_deal(buyer_id,request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a deal
            return deals.put_deal(buyer_id,request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a deal
            return deals.delete_deal(buyer_id,request.args['_id'],client)


    @app.route('/submit-seller', methods=['POST','PUT'])
    @requires_auth
    def submit_seller(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'POST':
            #retrieve seller
            return sellers.post_seller(buyer_id,request,client)
        elif request.method == 'PUT':
            # Update a seller
            seller_id=request.args.get('_id')
            return sellers.put_seller(buyer_id,seller_id,request,client)
    @app.route('/sellers', methods=['GET'])
    @requires_auth
    def manage_seller(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return sellers.list_all_sellers(buyer_id,client)

    @app.route('/seller', methods=['GET', 'PUT', 'DELETE'])
    @requires_auth
    def process_seller(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            #retrieve seller
            return sellers.get_seller(buyer_id,request.args['_id'],client)
        elif request.method == 'PUT':
            # Update a seller
            return sellers.put_seller(buyer_id,request.args['_id'],request.json,client)
    
        elif request.method == 'DELETE':
            # Delete a seller
            return sellers.delete_seller(buyer_id,seller_name,client)





    # Example of a protected route
    @app.route('/')
    def your_protected_route():
        # Now this route only requires the user to be authenticated
        return 'Welcome to Another DSP API'

if __name__ == '__main__':
    app.run(debug=True)