# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lucas <lucas@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/25 11:58:59 by lucas             #+#    #+#              #
#    Updated: 2024/05/25 12:56:06 by lucas            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# import random
import pygame

# Init
pygame.init()

# window size
window_size = (1000, 1000)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")

# Définir les couleurs (R, G, B)
colors = {
    0: (255, 255, 255),  # Blanc
    1: (0, 0, 0),        # Noir
    2: (255, 0, 0),      # Rouge
    3: (0, 255, 0),      # Vert
    4: (0, 0, 255),      # Bleu
    # Ajouter d'autres couleurs pour les valeurs de 5 à 19
}

# map gen
map_size = 400
road_width = 8
center = map_size // 2
half_road = road_width // 2

# 100 x 100 + croisement
map_data = [[1 for _ in range(map_size)] for _ in range(map_size)]

for i in range(map_size):
    for j in range(center - half_road, center + half_road):
        map_data[i][j] = 0  # Route verticale
        map_data[j][i] = 0  # Route horizontale


# cell size
cell_size = window_size[0] / map_size  # Taille de cellule ajusté pour que la carte tienne dans la fenêtre

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill white
    window.fill((255, 255, 255))

    # draw map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Refresh
    pygame.display.flip()

# Leave
pygame.quit()
