# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    map_parser.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lucas <lucas@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/25 12:57:30 by lucas             #+#    #+#              #
#    Updated: 2024/05/25 13:39:39 by lucas            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pygame

# parser
def read_map(filename):
    with open(filename, 'r') as file:
        map_data = []
        for line in file:
            row = list(map(int, line.split()))
            map_data.append(row)
    return map_data

class Voiture:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest

    def move(self):
        if self.orientation == 0:  # Nord
            self.y -= self.vitesse
        elif self.orientation == 1:  # Est
            self.x += self.vitesse
        elif self.orientation == 2:  # Sud
            self.y += self.vitesse
        elif self.orientation == 3:  # Ouest
            self.x -= self.vitesse

    def draw(self, window, cell_size):
        # draw car as a red rectangle
        car_size = cell_size // 2
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_size, car_size)
        pygame.draw.rect(window, (255, 0, 0), car_rect)
        
# Init
pygame.init()

# win size
window_size = (1200, 1200)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")

# color / pixel
colors = {
    0: (0, 0, 0),        # Noir (route)
    1: (255, 255, 255),  # Blanc (autre)
    4: (255, 0 , 0),    # stop
}

# read
map_data = read_map('map.txt')
map_size = 10

# pixel size
cell_size = (window_size[0] // map_size) // 3

# main


# main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill default
    window.fill((255, 255, 255))

    # draw
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Refresh
    pygame.display.flip()

# Leave
pygame.quit()
