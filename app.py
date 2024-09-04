# app.py (using FastAPI)
import os
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Securely retrieve API key from environment variables
api_key = os.getenv('OPENWEATHER_API_KEY')
if not api_key:
    raise EnvironmentError("API key not found. Please set the OPENWEATHER_API_KEY environment variable.")

# Define endpoint to get weather data
@app.get("/weather")
def get_weather(city: str):
    # Construct the weather API URL
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    # Make request to external weather API
    response = requests.get(weather_url)

    # Check response status code
    if response.status_code == 200:
        weather_data = response.json()
        return {
            "temperature": weather_data['main']['temp'],
            "description": weather_data['weather'][0]['description'],
            "icon": weather_data['weather'][0]['icon']
        }
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"No weather data found for {city}. Please check the city name.")
    else:
        raise HTTPException(status_code=response.status_code, detail="Weather API returned an error.")
