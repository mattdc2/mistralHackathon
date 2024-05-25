import os

def load_dotenv():
    # Load environment variables from a .env file without using dotenv package
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value
