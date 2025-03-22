import os
from dotenv import load_dotenv
import requests
from pydantic import BaseModel
import json
load_dotenv()

AMADEUS_API_URL = os.getenv("AMADEUS_API_URL")
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
AMADEUS_ACCESS_TOKEN = os.getenv("AMADEUS_ACCESS_TOKEN")

flights_get_url="shopping/flight-offers"

class GETFlightsRequest(BaseModel):
    origin: str
    destination: str
    departure_date: str
    return_date: str
    adults: int

class Flight(BaseModel):
    price: int
    departure_date: str
    return_date: str
    departure_time: str
    arrival_time: str
    duration: str

def get_flights_api_call(request: GETFlightsRequest):
    url = f"{AMADEUS_API_URL}/{flights_get_url}"
    params = {
        "originLocationCode": request.origin,
        "destinationLocationCode": request.destination,
        "departureDate": request.departure_date,
        "adults": request.adults,
        "max": 10
    }
    headers = {
        "Authorization": f"Bearer {AMADEUS_ACCESS_TOKEN}"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()
        
        # Return the actual data list rather than a JSON string
        return response_json.get('data', [])
    except Exception as e:
        print(f"[error] API call failed: {str(e)}")
        return []