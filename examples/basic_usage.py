import os
from dotenv import load_dotenv
from deepseek import DeepSeekAPI

# Load environment variables
load_dotenv()

def main():
    # Initialize DeepSeek client
    client = DeepSeekAPI(api_key=os.getenv("DEEPSEEK_API_KEY"))
    
    # Example: Generate text
    prompt = "Write a short poem about artificial intelligence."
    response = client.chat_completion(prompt)
    
    print("Generated Text:")
    print(response)

if __name__ == "__main__":
    main() 