import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def main():
    # Initialize OpenAI client with DeepSeek's base URL
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    # Example: Generate text
    messages = [
        {"role": "user", "content": "Write a short poem about artificial intelligence."}
    ]
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    
    print("Generated Text:")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main() 