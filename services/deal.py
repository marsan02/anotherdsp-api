from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

def get_deal(buyer_id,deal_id,client):
    # Get a single deal
    # Select the database
    db = client['deals']
    deals = db.deals
    deal_id = ObjectId(deal_id)
    deal = deals.find_one({"_id": deal_id}, {'_id': 0})
    if deal:
        return jsonify(deal)
    else:
        return jsonify({"message": "deal not found" }), 404

def put_deal(buyer_id,deal_id,request,client):
    db = client['deals']
    deals = db.deals
    deal_id=ObjectId(deal_id)
    payload = prepare_data(request.get_json())[0]
    result = deals.update_one({"_id": deal_id}, {"$set": payload})
    if result.matched_count:
        print("updated")
        return jsonify({"message": "deal updated"})
    else:
        print("error)")
        return jsonify({"message": "deal not found"}), 404

def delete_deal(buyer_id,deal_name,client):
    db = client['deals']
    deals = db.deals
    result = deals.delete_one({"deal_name": deal_name})
    if result.deleted_count:
        return jsonify({"message": "deal deleted"})
    else:
        return jsonify({"message": "deal not found"}), 404

def list_all_deals(buyer_id,client):
    db = client['deals']
    deals = db.deals
    all_deals_with_id = list(deals.find({}))
    for item in all_deals_with_id:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_deals_with_id)

def post_deal(buyer_id,request,client):
    db = client['deals']
    deals = db.deals
    print("Submitting deal")
    try:

        deal_data = prepare_data(request.get_json())
        try:
            deals.insert_one(deal_data[0])
            return jsonify({"message": "deal added"}), 201
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
    name = data['name']
    seller_id = data['seller_id'] 
    buyer_id = data['buyer_id']
    deal_floor = data['deal_floor']
    deal_floor_curr = data['deal_floor_curr']
    price_type=data['price_type']
    code = data['code']

    # Create the data payload in the required format
    payload = [{
        "name": name,
        "seller_id": seller_id,
        "code": code,
        "buyer_id": buyer_id,
        "deal_floor": deal_floor,
        "prive_type": price_type,
        "deal_floor_curr": deal_floor_curr
        }]
    return payload
