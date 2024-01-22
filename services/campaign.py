from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

def get_campaign(buyer_id,campaign_id,client):
    # Get a single campaign
    # Select the database
    db = client['campaigns']
    campaigns = db.campaigns
    campaign_id = ObjectId(campaign_id)
    campaign = campaigns.find_one({"_id": campaign_id, "buyer_id":buyer_id}, {'_id': 0})
    if campaign:
        return jsonify(campaign)
    else:
        return jsonify({"message": "Campaign not found" }), 404

def put_campaign(buyer_id,campaign_id,request,client):
    db = client['campaigns']
    campaigns = db.campaigns
    campaign_id=ObjectId(campaign_id)
    print(request)
    payload = prepare_data(buyer_id,request.get_json())[0]
    result = campaigns.update_one({"_id": campaign_id, "buyer_id":buyer_id}, {"$set": payload})
    if result.matched_count:
        print("updated")
        return jsonify({"message": "Campaign updated"})
    else:
        print("error)")
        return jsonify({"message": "Campaign not found"}), 404

def delete_campaign(buyer_id,campaign_id,client):
    db = client['campaigns']
    campaigns = db.campaigns
    query = {"_id": ObjectId(campaign_id)}
    if buyer_id:
        query['buyer_id']=buyer_id
    result = campaigns.delete_one(query)
    if result.deleted_count:
        return jsonify({"message": "Campaign deleted"})
    else:
        return jsonify({"message": "Campaign not found"}), 404

def list_all_campaigns(buyer_id,client,filters):
    db = client['campaigns']
    campaigns = db.campaigns
    adv_id=filters.get('advertiser_id')
    query=dict({"buyer_id":buyer_id})
    if adv_id:
        query["advertiser_id"]= adv_id
    all_campaigns_with_id = list(campaigns.find(query))
    for item in all_campaigns_with_id:
        item["_id"] = str(item["_id"])
    return jsonify(all_campaigns_with_id)

def post_campaign(buyer_id,request,client):
    db = client['campaigns']
    campaigns = db.campaigns
    print("Submitting Campaign")
    try:

        campaign_data = prepare_data(buyer_id,request.get_json())

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

def prepare_data(buyer_id,data):
        # Extract form data
    campaign_name = data['campaign_name']
    adv = data.get('advertiser_id')
    if adv:
        advertiser_id=data['advertiser_id']
    ad_types = data['ad_types']
    creatives = data['creatives']
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
    inventory = data['inventory']
    deals = data['deals']

    # Create the data payload in the required format
    payload = [{
        "ad_types": ad_types,
        "advertiser_id": adv,
        "campaign_name": campaign_name,
        "creatives": creatives,
        "device_types": device_types,
        "flight_dates": {
            "start": start_date,
            "end": end_date
        },
        "buyer_id": buyer_id,
        "geography": geography,
        "inventory_type": inventory_type,
        "revenue_per_day": revenue_per_day,
        "state": state,
        "total_budget": total_budget,
        "goal_type":goal_type,
        "goal_value":goal_value,
        "inventory":inventory,
        "deals": deals
        }]
    return payload
