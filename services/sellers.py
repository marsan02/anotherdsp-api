from flask import Flask, request, jsonify, request, render_template, redirect,url_for
import requests
from bson import ObjectId
from services.generic_service import BaseAPIService

class SellersService(BaseAPIService):
    def __init__(self,client):
        super().__init__(
            database = "sellers",
            schema = {"name":str},
            client = client
        )