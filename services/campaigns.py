from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService
import numbers

class CampaignsService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "campaigns",
            schema = {"campaign_name":str,
            "ad_type": int,
            "creatives": list,
            "device_types": list,
           "geography": list,
            "inventory_type": list,
            "daily_budget": numbers.Number,
            "total_budget": numbers.Number,
            "state": str,
            "goal_type": str,
            "goal_value": numbers.Number,
            "inventory": list,
            "deals": list,
            "start_date": str,
            "end_date": str,
            "advertiser_id": str,
            "buyer_id": str       
            },
            client = client
        )