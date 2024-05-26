import json
import time

import pygame
from utils import read_map, print_matrix, convert_pos_to_index
from self_driving_llm import translate_map_into_prompt
from mistral_api import ask_question

# PARAMS
# Please note that the top left of the map is (0, 0) and the bottom right is (30, 20)
# which means that y increases as we go down and x increases as we go right
max_x = 30.75
max_y = 20.75
min_x = -0.25
min_y = -0.25
range_x = max_x - min_x
range_y = max_y - min_y

map_size = 9
window_size = (1000, 600)

# color structure
colors = {
    3: (0, 0, 0),        # Noir (route)
    2: (255, 255, 255),  # Blanc (autre)
    9: (0, 0, 255),      # sens interdit (et bordures)
    5: (255, 0, 0),      # Feu rouge
    6: (0, 255, 0),      # Feu vert
    7: (255, 255, 0),    # Cédez le passage
    4: (0, 255, 255),    # piéton ou cycliste
}

initial_x = 15.75
initial_y = 3.75
initial_vitesse = 0.25
initial_orientation = 2


def get_position_and_action(map, voiture_b, voiture_f):
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
    assert window_size % 2 == 0, "The window size must be an even number"
    x, y = convert_pos_to_index(voiture_f.x), convert_pos_to_index(voiture_f.y)
    start_line = max(0, y - window_size // 2)
    end_line = min(len(map), y + window_size // 2)
    start_col = max(0, x - window_size // 2)
    end_col = min(len(map[0]), x + window_size // 2)

    smaller_map = [map[i][start_col:end_col] for i in range(start_line, end_line)]
    return smaller_map


def add_example_in_txt(map, action, json_path="data/training_data.json"):
    with open(json_path, "r") as file:
        data = json.load(file)
        data['messages'].append({'role': 'user', 'content': f"La carte est la suivante : {map}. Que devrais-tu faire ? Repondre sous la forme d'une action parmi les 5 actions possibles."})
        data['messages'].append({'role': 'assistant', 'content': action})
    with open(json_path, "w") as out_file:
        out_file.write(json.dumps(data))


def create_action_from_direction(direction: str):
    # we want to translate the direction of the car into an action
    # direction is one of "S'arreter", "Avancer", "Tourner a gauche", "Tourner a droite", "Faire demi-tour"
    # if the car is going East and the LLM says "go straight", the action will be "KEY_RIGHT"
    # if the car is going East and the LLM says "turn left", the action will be "KEY_UP"
    if direction == "s'arreter":
        return 0  # action to stop
    elif direction == "avancer tout droit":
        if voiture_f.orientation == 0:  # North
            return 1  # action to go up
        elif voiture_f.orientation == 1:  # West
            return 3  # action to go left
        elif voiture_f.orientation == 2:  # South
            return 2  # action to go down
        elif voiture_f.orientation == 3:  # East
            return 4  # action to go right
    elif direction == "tourner a gauche":
        if voiture_f.orientation == 0:
            return 3
        elif voiture_f.orientation == 1:
            return 2
        elif voiture_f.orientation == 2:
            return 4
        elif voiture_f.orientation == 3:
            return 1
    elif direction == "tourner a droite":
        if voiture_f.orientation == 0:
            return 4
        elif voiture_f.orientation == 1:
            return 1
        elif voiture_f.orientation == 2:
            return 3
        elif voiture_f.orientation == 3:
            return 2
    elif direction == "reculer":
        if voiture_f.orientation == 0:
            return 2
        elif voiture_f.orientation == 1:
            return 4
        elif voiture_f.orientation == 2:
            return 1
        elif voiture_f.orientation == 3:
            return 3


class Voiture_F:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest
        self.prev_orientation = orientation

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y
        if self.orientation == 0:  # North
            self.y -= 1
            self.x = self.x

        elif self.orientation == 1:  # West
            self.x -= 1
            self.y = self.y

        elif self.orientation == 2:  # South
            self.y += 1
            self.x = self.x

        elif self.orientation == 3:  # East
            self.x += 1
            self.y = self.y

    def interpreteur(self, retour):
            # 0 = stop
            # 1 = go up
            # 2 = go down
            # 3 = go left
            # 4 = go right
            if retour == 0:
                self.vitesse = 0
                voiture_b.vitesse = 0
                self.y = self.y
                self.x = self.x
            if retour == 1:
                self.y -= 1
                self.x = self.x
            if retour == 2:
                self.y += 1
                self.x = self.x
            if retour == 3:
                self.x -= 1
                self.y = self.y
            if retour == 4:
                self.x += 1
                self.y = self.y

    def stay(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_orientation = self.orientation

    def draw(self, window, cell_size):
        car_width = cell_size
        car_len = cell_size
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)


class Voiture_B:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest
        self.prev_orientation = orientation

    def move(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_orientation = self.orientation

        self.x = voiture_f.x
        self.y = voiture_f.y

    def stay(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.prev_orientation = self.orientation

    def interpreteur(self, retour):
        # 0 = stop
        # 1 = go up
        # 2 = go down
        # 3 = go left
        # 4 = go right
        if retour == 0: 
            self.x = self.x
            self.y = self.y
        elif retour == 1:
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif retour == 2:
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif retour == 3:
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif retour == 4:
            self.x = voiture_f.x
            self.y = voiture_f.y
    
    def draw(self, window, cell_size):
        # Dessiner la voiture comme un rectangle rouge
        car_width = cell_size
        car_len = cell_size
        # elif self.orientation == 1 or self.orientation == 3:
        #     car_len = cell_size
        #     car_width = car_len * 2
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (0, 255, 0), car_rect)


    
# Init
pygame.init()

# window init
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")

# read
map_data = read_map('data/map4.txt')

# pixel size
cell_size = window_size[0] // map_size // 4

# Position initiale (1, 1), vitesse 0.02, orientation Est = 1
voiture_f = Voiture_F(initial_x, initial_y, initial_vitesse, initial_orientation)
voiture_b = Voiture_B(voiture_f.x, voiture_f.y - 1, voiture_f.vitesse, voiture_f.orientation)

# main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection des touches pour changer la direction de la voiture
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # reset
                voiture_f.x = 16.75
                voiture_f.y = 0.75
                voiture_b.x = 16.75
                voiture_b.y = 0.75 - 1
                voiture_f.orientation = 0
            elif event.key == pygame.K_RETURN:  # save example
                map_data, action = get_position_and_action(map_data, voiture_b, voiture_f)
                smaller_map = crop_map(map_data)
                add_example_in_txt(smaller_map, action)
                print("Action : ", action)
            else:  # move
                voiture_f.prev_orientation = voiture_f.orientation
                if event.key == pygame.K_DOWN:
                    voiture_f.orientation = 2  # South
                    voiture_b.move()
                    voiture_f.move()
                elif event.key == pygame.K_LEFT:
                    voiture_f.orientation = 1  # West
                    voiture_b.move()
                    voiture_f.move()
                elif event.key == pygame.K_UP:
                    voiture_f.orientation = 0  # North
                    voiture_b.move()
                    voiture_f.move()
                elif event.key == pygame.K_RIGHT:
                    voiture_f.orientation = 3  # East
                    voiture_b.move()
                    voiture_f.move()
                elif event.key == pygame.K_BACKSPACE:
                    voiture_f.stay()
                    voiture_b.stay()
                elif event.key == pygame.K_m:
                    cropped_map = crop_map(map_data, 6)
                    prompt = translate_map_into_prompt(cropped_map)
                    llm_input = ask_question(prompt).lower().replace("à", "a").replace(".", "")

                    result = create_action_from_direction(llm_input)

                    voiture_b.interpreteur(result)
                    voiture_f.interpreteur(result)
                    print('llm_input : ', llm_input)
                    print("Result : ", result)

    # fill default
    window.fill((255, 255, 255))

    # draw map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # draw car
    voiture_b.draw(window, cell_size)
    voiture_f.draw(window, cell_size)
    # Refresh
    pygame.display.flip()

# Leave
pygame.quit()
