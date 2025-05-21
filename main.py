import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

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
    # Initialize OpenAI client with DeepSeek's base URL
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    # Define available tools
    tools = [
        {
            "type": "function",
            "function": {
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
        }
    ]
    
    # Example conversation
    messages = [
        {"role": "user", "content": "What's the weather like in Guangzhou?"}
    ]
    
    # Get response from DeepSeek with function calling
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    # Process the response
    message = response.choices[0].message
    print(f"Model response: {message}")
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "get_weather":
            result = get_weather(function_args["city"])
            print(f"Weather result: {result}")
            
            # Add the function result to messages and get final response
            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
            
            final_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                tools=tools
            )
            print(f"Final response: {final_response.choices[0].message.content}")
    else:
        print(f"Direct response: {message.content}")

if __name__ == "__main__":
    main()