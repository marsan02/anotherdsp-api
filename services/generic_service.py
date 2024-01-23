from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId

class BaseAPIService:
    def __init__(self,database,schema,client):
        self.database = database
        self.schema = schema
        self.client = client

    def get(self, filters,object_id):
        db = self.client[self.database]
        collection = db[self.database]
        query = {}
        for filter in filters:
            if filter in self.schema:
                query[filter.field] = filter.value
        if object_id:
            query["_id"]=ObjectId(object_id)
        result = collection.find(query)

        # Convert the result to a list of dictionaries
        result_list = list(result)
        for item in result_list:
            item["_id"] = str(item["_id"])
        
        if result_list:
            # Serialize the list of dictionaries to JSON
            if object_id:
                return jsonify(result_list[0])
            else:
                return jsonify(result_list)
        else:
            return jsonify({"message": "object not found"}), 404


    def post(self, request,buyer_id):
        db = self.client[self.database]
        objects = db[self.database]
        print("Submitting Object")
        try:
            object_data = self.prepare_data(request,buyer_id)
            try:
                objects.insert_one(object_data)
                return jsonify({"message": "object added"}), 201
            except Exception as e:
                # If an error occurs, print the error and return an appropriate response
                print("Error occurred:", e)
                return jsonify({"error": str(e)}), 500           
        except Exception as e:
            # Handle exceptions
            print(e)
            return str(e), 500

    def put(self, object_id, request,buyer_id):
        db = self.client[self.database]
        objects = db[self.database]
        object_id = ObjectId(object_id)
        print("Submitting Object")
        payload = self.prepare_data(request,buyer_id)
        result = objects.update_one({"_id": object_id}, {"$set": payload})
        if result.matched_count:
            print("updated")
            return jsonify({"message": "object updated"})
        else:
            print("error)")
            return jsonify({"message": "object not found"}), 404

    def delete(self,object_id,buyer_id):
        db = self.client[self.database]
        objects = db[self.database]
        query = {"_id": ObjectId(object_id)}
        if buyer_id:
            query['buyer_id']=buyer_id
        result = objects.delete_one(query)
        if result.deleted_count:
            return jsonify({"message": "Object deleted"})
        else:
            return jsonify({"message": "Object not found"}), 404
    
    def prepare_data(self,data,buyer_id):
        # Extract form data
        payload={}
        print(data)
        for item in self.schema:
            print(item)
            value = data.get(item)
            print(value)
            print(type(value))
            item_type = self.schema[item]
            print(item_type)
            if isinstance(value, item_type):
                payload[item]=value
        print(payload)
        return payload

