from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests

def get_campaign(campaign_name,client):
    # Get a single campaign
    # Select the database
    db = client['campaigns']
    campaigns = db.campaigns
    campaign = campaigns.find_one({"campaign_name": campaign_name}, {'_id': 0})
    if campaign:
        return jsonify(campaign)
    else:
        return jsonify({"message": "Campaign not found" }), 404

def put_campaign(campaign_name,update_data,client):
    db = client['campaigns']
    campaigns = db.campaigns
    result = campaigns.update_one({"campaign_name": campaign_name}, {"$set": updated_data})
    if result.matched_count:
        return jsonify({"message": "Campaign updated"})
    else:
        return jsonify({"message": "Campaign not found"}), 404

def delete_campaign(campaign_name,client):
    db = client['campaigns']
    campaigns = db.campaigns
    result = campaigns.delete_one({"campaign_name": campaign_name})
    if result.deleted_count:
        return jsonify({"message": "Campaign deleted"})
    else:
        return jsonify({"message": "Campaign not found"}), 404

def list_all_campaigns(client):
    db = client['campaigns']
    campaigns = db.campaigns
    all_campaigns = list(campaigns.find({}, {'_id': 0}))
    return jsonify(all_campaigns)

def post_campaign(request,client):
    db = client['campaigns']
    campaigns = db.campaigns
    print("Submitting Campaign")
    try:
        # Extract form data
        data = request.get_json()
        campaign_name = data['campaign_name']
        ad_types = data['ad_types']
        creatives = data['creatives'].split(',')
        device_types = data['device_types']
        geography = data['geography']
        inventory_type = data['inventory_type']
        revenue_per_day = int(data['revenue_per_day'])
        state = data['state']
        total_budget = int(data['total_budget'])
        start_date = data['start_date']
        end_date = data['end_date']
        goal_type = data['goal_type']
        goal_value= data['goal_value']

        # Create the data payload in the required format
        payload = [{
            "ad_types": ad_types,
            "campaign_name": campaign_name,
            "creatives": creatives,
            "device_types": device_types,
            "flight_dates": {
                "start": start_date,
                "end": end_date
            },
            "geography": geography,
            "inventory_type": inventory_type,
            "revenue_per_day": revenue_per_day,
            "state": state,
            "total_budget": total_budget,
            "goal_type":goal_type,
            "goal_value":goal_value
        }]
        print(payload)
        campaign_data = payload
        try:
            campaigns.insert_one(campaign_data[0])
            return jsonify({"message": "Campaign added"}), 201
        except Exception as e:
            # If an error occurs, print the error and return an appropriate response
            print("Error occurred:", e)
            return jsonify({"error": str(e)}), 500           
    except Exception as e:
        # Handle exceptions
        print(e)
        return str(e), 500
