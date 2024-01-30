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
import pypyodbc
from utils.mysql_connection import Database


load_dotenv()  # This loads the environment variables from .env



def configure_routes(app):


    # MongoDB Atlas connection URI
    mongo_uri = os.environ.get("MONGO_URI")
    client = MongoClient(mongo_uri)

    try:
        # Connection string
        #connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={mysql_server};DATABASE={mysql_database};UID={mysql_username};PWD={mysql_password}'
        mysql_conn = Database()
        #mysql_conn= connection_string
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
            if not buyer_id:
                buyer_id = request.args.get('buyer_id')
            if buyer_id:
                buyer_id=int(buyer_id)
            all_campaigns, status = campaigns.get_mysql(request.args, request.args.get('id'),buyer_id,mysql_conn)
            payload = {
                "dimensions": ["campaign_id"],
                "metrics": ["bids", "imps", "clicks", "viewable_imps", "spend", "revenue"],
                "filters": []
            }
            reporting_data = reporting.run_report(buyer_id, payload['dimensions'], payload['metrics'], payload['filters'])

            # Create a lookup for campaign reporting data
            reporting_lookup = {report['campaign_id']: report for report in reporting_data}

            stitched_data = []
            if status == 200:
                for campaign in all_campaigns:
                    campaign_id = campaign['id']
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
            else:
                return jsonify({"message": "object not found"}), 404      

        @app.route('/campaigns', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def campaigns_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if not buyer_id:
                buyer_id = request.args.get('buyer_id')
            if buyer_id:
                buyer_id=int(buyer_id)
            if request.method == 'GET':
                return campaigns.get_mysql(request.args,request.args.get('id'),buyer_id,mysql_conn)
            elif request.method == 'PUT':
                return campaigns.put_mysql(request.args['id'],request.json,buyer_id,mysql_conn)
            elif request.method == 'DELETE':
                return campaigns.get_mysql(request.args['id'],buyer_id,mysql_conn)
            elif request.method == 'POST':
                return campaigns.post_mysql(request.json,buyer_id,mysql_conn)
        
        @app.route('/advertisers', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def advertisers_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if not buyer_id:
                buyer_id = request.args.get('buyer_id')
            if buyer_id:
                buyer_id=int(buyer_id)
            if request.method == 'GET':
                result =  advertisers.get_mysql(request.args,request.args.get('id'),1,mysql_conn)
            elif request.method == 'PUT':
                result = advertisers.put_mysql(request.args['id'],request.json,1,mysql_conn)
            elif request.method == 'DELETE':
                result = advertisers.delete_mysql(request.args['id'],1,mysql_conn)
            elif request.method == 'POST':
                result = advertisers.post_mysql(request.json,1,mysql_conn)
            return result
                    
        @app.route('/deals', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def deals_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if not buyer_id:
                buyer_id = request.args.get('buyer_id')
            if buyer_id:
                buyer_id=int(buyer_id)            
            if request.method == 'GET':
                result =  deals.get_mysql(request.args,request.args.get('id'),buyer_id,mysql_conn)
            elif request.method == 'PUT':
                result = deals.put_mysql(request.args['id'],request.json,buyer_id,mysql_conn)
            elif request.method == 'DELETE':
                result= deals.delete_mysql(request.args['id'],buyer_id,mysql_conn)
            elif request.method == 'POST':
                result= deals.post_mysql(request.json,buyer_id,mysql_conn)
            return result

        @app.route('/creatives', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def creatives_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if not buyer_id:
                buyer_id = request.args.get('buyer_id')
            if buyer_id:
                buyer_id=int(buyer_id)
            if request.method == 'GET':
                result= creatives.get_mysql(request.args,request.args.get('id'),buyer_id,mysql_conn)
            elif request.method == 'PUT':
                result= creatives.put_mysql(request.args['id'],request.json,buyer_id,mysql_conn)
            elif request.method == 'DELETE':
                result= creatives.delete_mysql(request.args['id'],buyer_id,mysql_conn)
            elif request.method == 'POST':
                result= creatives.post_mysql(request.json,buyer_id,mysql_conn)
            return result

        @app.route('/sellers', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def sellers_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if request.method == 'GET':
                result= sellers.get_mysql(request.args,request.args.get('id'),buyer_id,mysql_conn)
            elif request.method == 'PUT':
                result= sellers.put_mysql(request.args['id'],request.json,buyer_id,mysql_conn)
            elif request.method == 'DELETE':
                result= sellers.delete_mysql(request.args['id'],buyer_id,mysql_conn)
            elif request.method == 'POST':
                result= sellers.post_mysql(request.json,buyer_id,mysql_conn)
            return result

        @app.route('/buyers', methods=['POST','GET', 'PUT', 'DELETE'])
        @requires_auth
        def buyers_service(*args, **kwargs):
            buyer_id = kwargs.get('buyer_id', None)
            if request.method == 'GET':
                result= buyers.get_mysql(request.args,request.args.get('id'),buyer_id,mysql_conn)
            elif request.method == 'PUT':
                result= buyers.put_mysql(request.args['id'],request.json,buyer_id,mysql_conn)
            elif request.method == 'DELETE':
                result= buyers.delete(request.args['id'],buyer_id)
            elif request.method == 'POST':
                result= buyers.post_mysql(request.json,buyer_id,mysql_conn)
            return result
        # Example of a protected route
    
        @app.route('/')
        def your_protected_route():
            # Now this route only requires the user to be authenticated
            return 'Welcome to Another DSP API'
    except pypyodbc.Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)