from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

def get_seller(seller_id,client):
    # Get a single seller
    # Select the database
    db = client['sellers']
    sellers = db.sellers
    seller_id = ObjectId(seller_id)
    seller = sellers.find_one({"_id": seller_id}, {'_id': 0})
    if seller:
        return jsonify(seller)
    else:
        return jsonify({"message": "seller not found" }), 404

def put_seller(seller_id,request,client):
    db = client['sellers']
    sellers = db.sellers
    seller_id=ObjectId(seller_id)
    payload = prepare_data(request.get_json())[0]
    result = sellers.update_one({"_id": seller_id}, {"$set": payload})
    if result.matched_count:
        print("updated")
        return jsonify({"message": "seller updated"})
    else:
        print("error)")
        return jsonify({"message": "seller not found"}), 404

def delete_seller(seller_name,client):
    db = client['sellers']
    sellers = db.sellers
    result = sellers.delete_one({"seller_name": seller_name})
    if result.deleted_count:
        return jsonify({"message": "seller deleted"})
    else:
        return jsonify({"message": "seller not found"}), 404

def list_all_sellers(client):
    db = client['sellers']
    sellers = db.sellers
    all_sellers_with_id = list(sellers.find({}))
    for item in all_sellers_with_id:
        print(item)
        item["_id"] = str(item["_id"])
    return jsonify(all_sellers_with_id)

def post_seller(request,client):
    db = client['sellers']
    sellers = db.sellers
    print("Submitting seller")
    try:

        seller_data = prepare_data(request.get_json())
        try:
            sellers.insert_one(seller_data[0])
            return jsonify({"message": "seller added"}), 201
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
