from flask import Flask, request, jsonify, request, render_template, redirect,url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from flask_cors import CORS
import utils.geo_api as geo_api
import requests
from utils.auth import requires_auth, handle_auth_error, AuthError
import os
import services.reporting as reporting
from services.sellers import SellersService
from services.buyers import BuyersService
from services.deals import DealsService
from services.creatives import CreativesService
from services.campaigns import CampaignsService
from services.advertisers import AdvertisersService



load_dotenv()  # This loads the environment variables from .env



def configure_routes(app):


    # MongoDB Atlas connection URI
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)
    app.register_error_handler(AuthError, handle_auth_error)
    sellers = SellersService(client)
    buyers = BuyersService(client)
    deals = DealsService(client)
    creatives = CreativesService(client)
    campaigns = CampaignsService(client)
    advertisers = AdvertisersService(client)

    @app.route('/countries')
    @requires_auth
    def get_countries(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        return geo_api.get_countries()

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
        all_campaigns = campaigns.get(request.args, request.args.get('_id'))
        payload = {
            "dimensions": ["campaign_id"],
            "metrics": ["bids", "imps", "clicks", "viewable_imps", "spend", "revenue"],
            "filters": []
        }
        reporting_data = reporting.run_report(buyer_id, payload['dimensions'], payload['metrics'], payload['filters'])
        all_campaigns = all_campaigns.json

        # Create a lookup for campaign reporting data
        reporting_lookup = {report['campaign_id']: report for report in reporting_data}

        stitched_data = []
        for campaign in all_campaigns:
            campaign_id = campaign['_id']
            if campaign_id in reporting_lookup:
                # Merge the dictionaries (Python 3.5+)
                merged = {**campaign, **reporting_lookup[campaign_id]}
            else:
                # Create a record with all metrics set to 0 for campaigns without reporting data
                metrics_zero = {metric: 0 for metric in payload['metrics']}
                metrics_zero['campaign_id'] = campaign_id
                merged = {**campaign, **metrics_zero}

            stitched_data.append(merged)

        return stitched_data

    @app.route('/campaigns', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def campaigns_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return campaigns.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return campaigns.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return campaigns.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return campaigns.post(request.json,buyer_id)
    
    @app.route('/advertisers', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def advertisers_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return advertisers.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return advertisers.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return advertisers.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return advertisers.post(request.json,buyer_id)  
                 
    @app.route('/deals', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def deals_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return deals.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return deals.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return deals.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return deals.post(request.json,buyer_id)
    
    @app.route('/creatives', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def creatives_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return creatives.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return creatives.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return creatives.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return creatives.post(request.json,buyer_id)

    @app.route('/sellers', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def sellers_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return sellers.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return sellers.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return sellers.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return sellers.post(request.json,buyer_id)

    @app.route('/buyers', methods=['POST','GET', 'PUT', 'DELETE'])
    @requires_auth
    def buyers_service(*args, **kwargs):
        buyer_id = kwargs.get('buyer_id', None)
        if request.method == 'GET':
            return buyers.get(request.args,request.args.get('_id'))
        elif request.method == 'PUT':
            return buyers.put(request.args['_id'],request.json,buyer_id)
        elif request.method == 'DELETE':
            return buyers.delete(request.args['_id'],buyer_id)
        elif request.method == 'POST':
            return buyers.post(request.json,buyer_id)
    # Example of a protected route
   
    @app.route('/')
    def your_protected_route():
        # Now this route only requires the user to be authenticated
        return 'Welcome to Another DSP API'

if __name__ == '__main__':
    app.run(debug=True)