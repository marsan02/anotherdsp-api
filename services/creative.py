from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId


def get_creative(client, filters):
    # Select the database and collection
    db = client['creatives']
    creatives = db.creatives

    # Construct a dynamic query based on the filters
    query = {}
    for filter in filters:
        field_name = filter.get("field_name")
        filter_value = filter.get("filter_value")
        query[field_name] = filter_value
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

def put_creative(creative_name,update_data,client):
    db = client['creatives']
    creatives = db.creatives
    result = creatives.update_one({"creative_name": creative_name}, {"$set": updated_data})
    if result.matched_count:
        return jsonify({"message": "creative updated"})
    else:
        return jsonify({"message": "creative not found"}), 404

def delete_creative(creative_name,client):
    db = client['creatives']
    creatives = db.creatives
    result = creatives.delete_one({"creative_name": creative_name})
    if result.deleted_count:
        return jsonify({"message": "creative deleted"})
    else:
        return jsonify({"message": "creative not found"}), 404

def list_all_creatives(client):
    db = client['creatives']
    creatives = db.creatives
    all_creatives = list(creatives.find({}))
    for item in all_creatives:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_creatives)

    return jsonify(all_creatives)

def post_creative(request,client):
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

        payload = [{
            "name": name,
            "width": width,
            "height": height,
            "type": creative_type,
            "asset_url": asset_url,
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
