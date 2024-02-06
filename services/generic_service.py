from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
import json

class BaseAPIService:
    def __init__(self,database,schema,client):
        self.database = database
        self.schema = schema
        self.client = client

    def get(self, filters,object_id,buyer_id):
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
    def get_mysql(self, filters,object_id,buyer_id,conn):
        # Executing an SQL command
        columns = ', '.join(self.schema.keys())
        query_filters = ''
        for filter in filters:
            if filter in self.schema:
                query_filters = query_filters + f' AND {filter}={filters[filter]}'
        if object_id:
            query_filters = query_filters + f' AND id={object_id}'
        if buyer_id and self.database !='buyers':
            query_filters = query_filters + f' AND buyer_id={buyer_id}'
        if buyer_id and self.database =='buyers':
            query_filters = query_filters + f' AND id={buyer_id}'

        query = f'SELECT {columns},last_edit,created_at FROM {self.database} WHERE 1=1 AND deleted=0 {query_filters}'
        print(query)
        result_list = conn.ExecQuery(query)
        if result_list:
            # Serialize the list of dictionaries to JSON
            if object_id:
                return result_list[0], 200
            else:
                return result_list, 200
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
    def post_mysql(self, request, buyer_id, conn):
        try:
            object_data = self.prepare_data(request, buyer_id)
            columns_list = list(object_data.keys())
            values_list = list(object_data.values())

            if buyer_id and self.database != 'buyers':
                columns_list.append("buyer_id")
                values_list.append(buyer_id)

            values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in values_list])
            columns = ', '.join(columns_list)
            insert_statement = f"INSERT INTO {self.database} ({columns}) VALUES ({values});"
            print(insert_statement)
            # Assuming conn is a valid database connection object
            conn.ExecNoQuery(insert_statement)

            return jsonify({"message": "object added"}), 201

        except Exception as e:
            # Rollback in case of error
            error_message = str(e)
            return jsonify({"error": error_message}), 500

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
    def put_mysql(self, object_id, request,buyer_id,conn):
        try:
            object_data = self.prepare_data(request, buyer_id)
            columns = ', '.join(object_data.keys())
            values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in object_data.values()])
            query_filters = f'id = {object_id}'
            if buyer_id and self.database !='buyers':
                query_filters = query_filters + f" AND buyer_id={buyer_id}"
            new_values = ', '.join([f"{col}='{val}'" if isinstance(val, str) else f'{col}={val}' for col, val in object_data.items()])
            update_statement = f"UPDATE {self.database} SET {new_values} WHERE {query_filters};"
            print(update_statement)
            # Assuming conn is a valid database connection object
            conn.ExecNoQuery(update_statement)

            return jsonify({"message": "object changed"}), 201

        except Exception as e:
            # Rollback in case of error
            conn.rollback()
            # Convert the error message to a string and return it in the API response
            error_message = str(e)
            return jsonify({"error": error_message}), 500
    def delete_mysql(self,object_id,buyer_id,conn):
        try:
            query_filters = f'id = {object_id}'
            if buyer_id and self.database !='buyers':
                query_filters = query_filters + f" AND buyer_id={buyer_id}"
            update_statement = f"UPDATE {self.database} SET deleted = 1 WHERE {query_filters};"
            print(update_statement)
            # Assuming conn is a valid database connection object
            conn.ExecNoQuery(update_statement)

            return jsonify({"message": "Object deleted"}), 201
        except Exception as e:
            # Rollback in case of error
            #conn.rollback()
            # Convert the error message to a string and return it in the API response
            error_message = str(e)
            return jsonify({"error": error_message}), 500
    
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
            value = data.get(item)
            item_type = self.schema[item]
            if isinstance(value, item_type):
                payload[item]=value
        return payload

