import os
from dotenv import load_dotenv
from deepseek import DeepSeekAPI

# Load environment variables
load_dotenv()

def main():
    # Initialize DeepSeek client
    client = DeepSeekAPI(api_key=os.getenv("DEEPSEEK_API_KEY"))
    
    print(client.user_balance())

if __name__ == "__main__":
    main() 