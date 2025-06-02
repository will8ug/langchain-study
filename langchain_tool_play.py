import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from tools.tools_weather import get_weather
from pydantic import BaseModel, Field

class GetWeather(BaseModel):
    city: str = Field(description="The city to get the weather for")

@tool(args_schema=GetWeather)
def get_weather_tool(city: str) -> str:
    """Get the current weather for a city."""
    return get_weather(city)

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize DeepSeek chat model
    chat = ChatDeepSeek(
        # api_key=os.getenv("DEEPSEEK_API_KEY"),
        model="deepseek-chat"
    )
    
    # Create chat with tools
    chat_with_tools = chat.bind_tools([get_weather_tool])
    
    # Example conversation
    response = chat_with_tools.invoke(
        "What's the weather like in Guangzhou?"
    )
    
    print("Model response:", response)
    print("tool_calls:", response.tool_calls)

    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        if tool_name == "get_weather_tool":
            # Use invoke instead of direct function call
            result = get_weather_tool.invoke({"city": tool_args["city"]})
            print("Weather result:", result)

if __name__ == "__main__":
    main() 