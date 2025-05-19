import os
import json
import requests
from dotenv import load_dotenv
from deepseek import DeepSeekAPI

# Load environment variables
load_dotenv()

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

def main():
    # Initialize DeepSeek client
    client = DeepSeekAPI(api_key=os.getenv("DEEPSEEK_API_KEY"))
    
    # Define available functions
    functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    ]
    
    # Example conversation
    messages = [
        {"role": "user", "content": "What's the weather like in Guangzhou?"}
    ]
    
    # Get response from DeepSeek with function calling
    response = client.chat_completion(
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    print(response)
    
    # Process the response
    if response.get("function_call"):
        function_name = response["function_call"]["name"]
        function_args = json.loads(response["function_call"]["arguments"])
        
        if function_name == "get_weather":
            result = get_weather(function_args["city"])
            print(result)
    else:
        print(response["content"])

if __name__ == "__main__":
    main()