from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId


def get_creative(buyer_id,client, filters):
    # Select the database and collection
    db = client['creatives']
    creatives = db.creatives
    adv_id=filters.get('advertiser_id')
    query=dict({"buyer_id":buyer_id})
    if adv_id:
        query["advertiser_id"]= adv_id
    all_creatives = list(creatives.find(query))
    print(query)
    # Find the creative(s) that match the dynamic query
    all_creatives = list(creatives.find(query))
    for item in all_creatives:
        print(item)
        item["_id"] = str(item["_id"])
    if all_creatives:
        return jsonify(all_creatives)
    else:
        return jsonify({"message": "creative not found"}), 404

def put_creative(buyer_id,creative_name,update_data,client):
    db = client['creatives']
    creatives = db.creatives
    result = creatives.update_one({"creative_name": creative_name, "buyer_id":buyer_id}, {"$set": updated_data})
    if result.matched_count:
        return jsonify({"message": "creative updated"})
    else:
        return jsonify({"message": "creative not found"}), 404

def delete_creative(buyer_id,creative_name,client):
    db = client['creatives']
    creatives = db.creatives
    result = creatives.delete_one({"creative_name": creative_name,"buyer_id":buyer_id})
    if result.deleted_count:
        return jsonify({"message": "creative deleted"})
    else:
        return jsonify({"message": "creative not found"}), 404

def list_all_creatives(buyer_id,client,filters):
    db = client['creatives']
    creatives = db.creatives
    adv_id=filters.get('advertiser_id')
    query=dict({"buyer_id":buyer_id})
    if adv_id:
        query["advertiser_id"]= adv_id
    all_creatives = list(creatives.find(query))
    for item in all_creatives:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_creatives)

    return jsonify(all_creatives)

def post_creative(buyer_id,request,client):
    db = client['creatives']
    creatives = db.creatives
    print("Submitting creative")
    try:
        # Extract form data
        data = request.get_json()
        name = data['name']
        width = data['width']
        height = data['height']
        creative_type = data['type']
        asset_url = data['asset_url']
        advertiser_id=data['advertiser_id']
        payload = [{
            "name": name,
            "width": width,
            "height": height,
            "type": creative_type,
            "asset_url": asset_url,
            "advertiser_id": advertiser_id,
            "buyer_id": buyer_id
        }]
        print(payload)
        creative_data = payload
        try:
            creatives.insert_one(creative_data[0])
            return jsonify({"message": "creative added"}), 201
        except Exception as e:
            # If an error occurs, print the error and return an appropriate response
            print("Error occurred:", e)
            return jsonify({"error": str(e)}), 500           
    except Exception as e:
        # Handle exceptions
        print(e)
        return str(e), 500
