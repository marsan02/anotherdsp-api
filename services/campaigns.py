from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService
import numbers

class CampaignsService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "campaigns",
            schema = {"name":str,
            "ad_type": int,
            "creatives": str,
            "daily_budget": numbers.Number,
            "total_budget": numbers.Number,
            "active": int,
            "goal_type": int,
            "goal_value": numbers.Number,
            "targeting": str,
            "start_date": str,
            "end_date": str,
            "advertiser_id": int,
            "buyer_id": int       
            },
            client = client
        )