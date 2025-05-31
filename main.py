import os
from dotenv import load_dotenv
from examples.raw_function_play import raw_func_play

# Load environment variables
load_dotenv()

def main():
    raw_func_play()

if __name__ == "__main__":
    main()