# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lucas <lucas@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/25 11:58:59 by lucas             #+#    #+#              #
#    Updated: 2024/05/25 12:04:37 by lucas            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pygame

# Init
pygame.init()

# window size
window_size = (800, 800)  # Ajuster la taille de la fenêtre si nécessaire
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("City")

# color / sprite for each
colors = {
    0: (255, 255, 255),  # Blanc
    1: (0, 0, 0),        # Noir
    2: (255, 0, 0),      # Rouge
    3: (0, 255, 0),      # Vert
    4: (0, 0, 255),      # Bleu
    # 5 6 7 8 ...
}

# gene map random
import random
map_size = 100
map_data = [[random.randint(0, 4) for _ in range(map_size)] for _ in range(map_size)]

# size pixel
cell_size = window_size[0] // map_size  # cell size to not overflow win size

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background fill
    window.fill((255, 255, 255))

    # Draw map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Refresh for each in loop
    pygame.display.flip()

# leave
# pygame.quit()
