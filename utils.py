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


def add_example_in_txt(map, action, json_path="data/training_data.json"):
    with open(json_path, "r") as file:
        data = json.load(file)
        data['messages'].append({'role': 'user', 'content': f"La carte est la suivante : {map}. Que devrais-tu faire ? Repondre sous la forme d'une action parmi les 5 actions possibles."})
        data['messages'].append({'role': 'assistant', 'content': action})
    with open(json_path, "w") as out_file:
        out_file.write(json.dumps(data))


def save_position_and_action_for_training(map, voiture_b, voiture_f):
    """
    Get the position of the car and deduce the right action to take from the last 2 positions
    """
    prev_x_b = convert_pos_to_index(voiture_b.prev_x)
    prev_y_b = convert_pos_to_index(voiture_b.prev_y)
    x_b = convert_pos_to_index(voiture_b.x)
    y_b = convert_pos_to_index(voiture_b.y)
    prev_x_f = convert_pos_to_index(voiture_f.prev_x)
    prev_y_f = convert_pos_to_index(voiture_f.prev_y)
    # first, add on the map the previous position of the car
    map[prev_y_b][prev_x_b] = 0
    map[prev_y_f][prev_x_f] = 1
    # then, figure out the action by looking at the difference between the current position and the previous one
    # we also need to check the orientation of the car, to know if it's going straight, back, or turning left or right
    new = voiture_f.orientation
    prev = voiture_f.prev_orientation
    if new == prev:
        if prev_x_b == x_b and prev_y_b == y_b:
            action = "S'arreter"
        else:
            action = "Avancer"
    elif (new == 0 and prev == 1) or (new == 1 and prev == 2) or (new == 2 and prev == 3) or (new == 3 and prev == 0):
        action = "Tourner a droite"
    elif (new == 0 and prev == 3) or (new == 1 and prev == 0) or (new == 2 and prev == 1) or (new == 3 and prev == 2):
        action = "Tourner a gauche"
    else:  # the car is going back
        action = "Faire demi-tour"
    return map, action


def crop_map(map, window_size=6):
    """
    Get a smaller window around the car, to generate training examples
    """
    assert window_size % 2 == 0, "The window size must be an even number"
    x, y = convert_pos_to_index(voiture_f.x), convert_pos_to_index(voiture_f.y)
    start_line = max(0, y - window_size // 2)
    end_line = min(len(map), y + window_size // 2)
    start_col = max(0, x - window_size // 2)
    end_col = min(len(map[0]), x + window_size // 2)

    smaller_map = [map[i][start_col:end_col] for i in range(start_line, end_line)]
    return smaller_map
