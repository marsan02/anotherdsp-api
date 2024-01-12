from geoip2.database import Reader
from dotenv import load_dotenv
import logging
import os
import pycountry


def initialize():
    load_dotenv()  # This loads the environment variables from .env
    # Initialize the GeoIP2 reader
    geoip_reader = Reader(os.environ.get("GEOLITE_PATH"))
    try:
        geoip_reader = Reader(os.environ.get("GEOLITE_PATH"))
    except Exception as e:
        logging.error(f"Error initializing GeoIP2 reader: {e}")
    return geoip_reader

def check_ip(geoip_reader,ip_address):
    response = geoip_reader.country(ip_address)
    (response)
    country = response.country.name
    return country

def get_countries():
    countries = [{"name":country.name, "code":country.alpha_2} for country in pycountry.countries]
    return(countries)

geoip_reader = initialize()
geoip_reader.close()
