from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService

class CreativesService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "creatives",
            schema = {"name":str,
            "width":int,
            "height":int,
            "ad_type":int,
            "asset_url":str,
            "advertiser_id": str,
            "landing_page_url": str},
            client = client
        )
        
