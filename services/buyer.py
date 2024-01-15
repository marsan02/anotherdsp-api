from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

def get_buyer(buyer_id,client):
    # Get a single buyer
    # Select the database
    db = client['buyers']
    buyers = db.buyers
    buyer_id = ObjectId(buyer_id)
    buyer = buyers.find_one({"_id": buyer_id}, {'_id': 0})
    if buyer:
        return jsonify(buyer)
    else:
        return jsonify({"message": "buyer not found" }), 404

def put_buyer(buyer_id,request,client):
    db = client['buyers']
    buyers = db.buyers
    buyer_id=ObjectId(buyer_id)
    payload = prepare_data(request.get_json())[0]
    result = buyers.update_one({"_id": buyer_id}, {"$set": payload})
    if result.matched_count:
        print("updated")
        return jsonify({"message": "buyer updated"})
    else:
        print("error)")
        return jsonify({"message": "buyer not found"}), 404

def delete_buyer(buyer_name,client):
    db = client['buyers']
    buyers = db.buyers
    result = buyers.delete_one({"buyer_name": buyer_name})
    if result.deleted_count:
        return jsonify({"message": "buyer deleted"})
    else:
        return jsonify({"message": "buyer not found"}), 404

def list_all_buyers(buyer_id,client):
    db = client['buyers']
    buyers = db.buyers
    buyer_id = ObjectId(buyer_id)
    all_buyers_with_id = list(buyers.find({"_id":buyer_id}))
    for item in all_buyers_with_id:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_buyers_with_id)

def post_buyer(request,client):
    db = client['buyers']
    buyers = db.buyers
    print("Submitting buyer")
    try:

        buyer_data = prepare_data(request.get_json())
        try:
            buyers.insert_one(buyer_data[0])
            return jsonify({"message": "buyer added"}), 201
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
    # Create the data payload in the required format
    payload = [{
        "name": name,
        }]
    return payload
