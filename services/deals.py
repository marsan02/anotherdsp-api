from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService
import numbers
class DealsService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "deals",
            schema = {"name":str,
            "seller_id":int,
            "code":str,
            "buyer_id":int,
            "deal_floor":numbers.Number,
            "currency": str,
            "deal_price_type_id": int},
            client = client
        )
        
