import json
import os


def load_dotenv():
    # Load environment variables from a .env file without using dotenv package
    with open(".env") as f:
        for line in f:
            key, value = line.strip().split("=")
            os.environ[key] = value


def load_json(path="data/mapping.json"):
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


def read_map(filename):
    with open(filename, 'r') as file:
        map_data = []
        for line in file:
            row = list(map(int, line.split()))
            map_data.append(row)
    return map_data


def print_matrix(matrix):
    for row in matrix:
        print(row)


def convert_pos_to_index(float_position) -> int:
    return int(float_position + 0.25)
