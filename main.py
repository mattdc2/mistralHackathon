# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lucas <lucas@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/25 15:15:24 by lucas             #+#    #+#              #
#    Updated: 2024/05/25 17:51:38 by lucas            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import json

import pygame


def get_position_and_action(map, voiture_b, voiture_f):
    # first, add on the map the previous position of the car
    x_b, y_b = int(voiture_b.prev_x // max_x), int(voiture_b.prev_y // max_y)
    x_f, y_f = int(voiture_f.prev_x // max_x), int(voiture_f.prev_y // max_y)
    map[y_b][x_b] = 0
    map[y_f][x_b] = 1
    # then, figure out the action by looking at the difference between the current position and the previous one
    # we also need to check the orientation of the car, to know if it's going straight, back, or turning left or right
    if voiture_f.x == voiture_f.prev_x and voiture_f.y == voiture_f.prev_y:
        action = "s'arreter"
    elif voiture_f.x == voiture_b.x and voiture_f.y == voiture_b.y:
        action = "reculer"
    elif voiture_f.prev_orientation == 0: # Nord
        if voiture_f.y < voiture_f.prev_y:
            action = "reculer"
        elif voiture_f.x < voiture_f.prev_x:
            action = "tourner a gauche"
        elif voiture_f.x > voiture_f.prev_x:
            action = "tourner a droite"
        elif voiture_f.y > voiture_f.prev_y:
            action = "avancer tout droit"
        else:
            action = "s'arreter"
    elif voiture_f.orientation == 1: # Est
        if voiture_f.x > voiture_f.prev_x:
            action = "avancer tout droit"
        elif voiture_f.y < voiture_f.prev_y:
            action = "tourner a gauche"
        else:
            action = "tourner a droite"
    elif voiture_f.orientation == 2: # Sud
        if voiture_f.y > voiture_f.prev_y:
            action = "avancer tout droit"
        elif voiture_f.x > voiture_f.prev_x:
            action = "tourner a gauche"
        else:
            action = "tourner a droite"
    elif voiture_f.orientation == 3: # Ouest
        if voiture_f.x < voiture_f.prev_x:
            action = "avancer tout droit"
        elif voiture_f.y > voiture_f.prev_y:
            action = "tourner a gauche"
        else:
            action = "tourner a droite"
    return map, action


def add_example_in_txt(map, action, json_path="training_data.json"):
    with open(json_path, "r") as file:
        data = json.load(file)
        data['messages'].append({'role': 'user', 'content': f"La carte est la suivante : {map}. Que devrais-tu faire ? Repondre sous la forme d'une action parmi les 5 actions possibles."})
        data['messages'].append({'role': 'assistant', 'content': action})
    with open(json_path, "w") as file:
        json.dump(data, file, indent=4)





# parser
def read_map(filename):
    with open(filename, 'r') as file:
        map_data = []
        for line in file:
            row = list(map(int, line.split()))
            map_data.append(row)
    return map_data




max_x = 30.75
max_y = 20.75





# Classe Voiture
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
        self.prev_orientation = self.orientation
        if self.orientation == 0:  # Nord
            self.y += 1
            self.x = self.x

        elif self.orientation == 1:  # Est
            self.x -= 1
            self.y = self.y

        elif self.orientation == 2:  # Sud
            self.y -= 1
            self.x = self.x

        elif self.orientation == 3:  # Ouest
            self.x += 1
            self.y = self.y

    def draw(self, window, cell_size):
        car_width = cell_size
        car_len = cell_size
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)


# Classe Voiture
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
        if self.orientation == 0:  # Nord
            self.x = voiture_f.x
            self.y = voiture_f.y
        elif self.orientation == 1:  # Est
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif self.orientation == 2:  # Sud
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif self.orientation == 3:  # Ouest
            self.y = voiture_f.y
            self.x = voiture_f.x
            
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
window_size = (1000, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")


# color structure
colors = {
    0: (0, 0, 0),        # Noir (route)
    1: (255, 255, 255),  # Blanc (autre)
    2: (0, 0, 255), 
    4: (255, 0, 0),      # Stop
}



# read
map_data = read_map('map.txt')
map_size = 9



# pixel size
cell_size = window_size[0] // map_size // 4




# Initialiser une voiture
voiture_f = Voiture_F(16.75, 0.75, 0.25, 0)  # Position initiale (1, 1), vitesse 0.02, orientation Est = 1 
voiture_b = Voiture_B(voiture_f.x, voiture_f.y - 1, voiture_f.vitesse, voiture_f.orientation)

# main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection des touches pour changer la direction de la voiture
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                voiture_f.orientation = 0  # Nord
                voiture_b.move()
                voiture_f.move()
            elif event.key == pygame.K_a:
                voiture_f.orientation = 1  # Est
                voiture_b.move()
                voiture_f.move()
            elif event.key == pygame.K_w:
                voiture_f.orientation = 2  # Sud
                voiture_b.move()
                voiture_f.move()
            elif event.key == pygame.K_d:
                voiture_f.orientation = 3  # Ouest
                voiture_b.move()
                voiture_f.move()
            elif event.key == pygame.K_SPACE:
                voiture_f.x = 16.75
                voiture_f.y = 0.75
                voiture_b.x = 16.75
                voiture_b.y = 0.75 - 1
                voiture_f.orientation = 0
            elif event.key == pygame.K_RETURN:
                map_data, action = get_position_and_action(map_data, voiture_b, voiture_f)
                add_example_in_txt(map_data, action)
                print("Action : ", action)
                print("Map : ", map_data)
                print("\n")


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
