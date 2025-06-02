import os
import requests
from dotenv import load_dotenv

def get_weather(city: str) -> str:
    """Get current weather for a city using OpenWeatherMap API."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeather API key not found in environment variables"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"  # For Celsius
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"The current weather in {city} is {weather} with a temperature of {temp}°C"
        else:
            return f"Error: Could not get weather for {city}"
    except Exception as e:
        return f"Error: {str(e)}" 