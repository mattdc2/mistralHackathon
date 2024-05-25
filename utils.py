import json
import os


def load_dotenv():
    # Load environment variables from a .env file without using dotenv package
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value


def load_mapping(path="mapping.json"):
    # Load mapping from a json file
    with open(path) as f:
        return json.load(f)


def load_map(path="map.txt"):
    # Load map from a text file
    map = []
    with open(path) as f:
        for line in f:
            map.append([cell for cell in line.strip().split()])
    return map
