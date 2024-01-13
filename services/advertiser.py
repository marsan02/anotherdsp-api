from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

def get_advertiser(advertiser_id,client):
    # Get a single advertiser
    # Select the database
    db = client['advertisers']
    advertisers = db.advertisers
    advertiser_id = ObjectId(advertiser_id)
    advertiser = advertisers.find_one({"_id": advertiser_id}, {'_id': 0})
    if advertiser:
        return jsonify(advertiser)
    else:
        return jsonify({"message": "advertiser not found" }), 404

def put_advertiser(advertiser_id,request,client):
    db = client['advertisers']
    advertisers = db.advertisers
    advertiser_id=ObjectId(advertiser_id)
    payload = prepare_data(request.get_json())[0]
    result = advertisers.update_one({"_id": advertiser_id}, {"$set": payload})
    if result.matched_count:
        print("updated")
        return jsonify({"message": "advertiser updated"})
    else:
        print("error)")
        return jsonify({"message": "advertiser not found"}), 404

def delete_advertiser(advertiser_name,client):
    db = client['advertisers']
    advertisers = db.advertisers
    result = advertisers.delete_one({"advertiser_name": advertiser_name})
    if result.deleted_count:
        return jsonify({"message": "advertiser deleted"})
    else:
        return jsonify({"message": "advertiser not found"}), 404

def list_all_advertisers(client):
    db = client['advertisers']
    advertisers = db.advertisers
    all_advertisers_with_id = list(advertisers.find({}))
    for item in all_advertisers_with_id:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_advertisers_with_id)

def post_advertiser(request,client):
    db = client['advertisers']
    advertisers = db.advertisers
    print("Submitting advertiser")
    try:

        advertiser_data = prepare_data(request.get_json())
        try:
            advertisers.insert_one(advertiser_data[0])
            return jsonify({"message": "advertiser added"}), 201
        except Exception as e:
            # If an error occurs, print the error and return an appropriate response
            print("Error occurred:", e)
            return jsonify({"error": str(e)}), 500           
    except Exception as e:
        # Handle exceptions
        print(e)
        return str(e), 500

def prepare_data(data):
        # Extract form data
    name = data['name']
    default_brand_url = data['default_brand_url'] 
    # Create the data payload in the required format
    payload = [{
        "name": name,
        "default_brand_url":default_brand_url
        }]
    return payload
