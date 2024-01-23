from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService

class AdvertisersService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "advertisers",
            schema = {"name":str,"default_brand_url":str},
            client = client
        )