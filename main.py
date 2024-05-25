# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: lucas <lucas@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/05/25 15:15:24 by lucas             #+#    #+#              #
#    Updated: 2024/05/25 17:10:26 by lucas            ###   ########.fr        #
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










# Classe Voiture
class Voiture_F:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest

    def move(self):
        if self.orientation == 0:  # Nord
            self.y -= self.vitesse
            print(self.y)
            print("N")
            print(self.x)
        elif self.orientation == 1:  # Est
            self.x += self.vitesse
            print(self.y)
            print("E")
            print(self.x)
        elif self.orientation == 2:  # Sud
            self.y += self.vitesse
            print(self.y)
            print("S")
            print(self.x)
        elif self.orientation == 3:  # Ouest
            self.x -= self.vitesse
            print(self.y)
            print('W')
            print(self.x)

            
    def can_move(self):
        try:
            if self.orientation == 0:  # Nord
                return self.map_data[self.y - 1][self.x] == 0 and self.map_data[self.y - 1][self.x - 1] == 1
            elif self.orientation == 1:  # Est
                return self.map_data[self.y][self.x + 1] == 0 and self.map_data[self.y - 1][self.x + 1] == 1
            elif self.orientation == 2:  # Sud
                return self.map_data[self.y + 1][self.x] == 0 and self.map_data[self.y + 1][self.x - 1] == 1
            elif self.orientation == 3:  # Ouest
                return self.map_data[self.y][self.x - 1] == 0 and self.map_data[self.y - 1][self.x - 1] == 1
        except IndexError:
            return False

    def draw(self, window, cell_size):
        # Dessiner la voiture comme un rectangle rouge
        if self.orientation == 0 or self.orientation == 2:
            car_width = cell_size
            car_len = car_width * 2
        elif self.orientation == 1 or self.orientation == 3:
            car_len = cell_size
            car_width = car_len * 2
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)


# Classe Voiture
class Voiture_B:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest

    def move(self):
        if self.orientation == 0:  # Nord
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif self.orientation == 1:  # Est
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif self.orientation == 2:  # Sud
            self.y = voiture_f.y
            self.x = voiture_f.x
        elif self.orientation == 3:  # Ouest
            self.y = voiture_f.y
            self.x = voiture_f.x
            
    def can_move(self):
        try:
            if self.orientation == 0:  # Nord
                return self.map_data[self.y - 1][self.x] == 0 and self.map_data[self.y - 1][self.x - 1] == 1
            elif self.orientation == 1:  # Est
                return self.map_data[self.y][self.x + 1] == 0 and self.map_data[self.y - 1][self.x + 1] == 1
            elif self.orientation == 2:  # Sud
                return self.map_data[self.y + 1][self.x] == 0 and self.map_data[self.y + 1][self.x - 1] == 1
            elif self.orientation == 3:  # Ouest
                return self.map_data[self.y][self.x - 1] == 0 and self.map_data[self.y - 1][self.x - 1] == 1
        except IndexError:
            return False

    def draw(self, window, cell_size):
        # Dessiner la voiture comme un rectangle rouge
        if self.orientation == 0 or self.orientation == 2:
            car_width = cell_size
            car_len = cell_size
        # elif self.orientation == 1 or self.orientation == 3:
        #     car_len = cell_size
        #     car_width = car_len * 2
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)




# Init
pygame.init()

# window init
window_size = (1620, 1080)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")


# color structure
colors = {
    0: (0, 0, 0),        # Noir (route)
    1: (255, 255, 255),  # Blanc (autre)
    4: (255, 0, 0),      # Stop
}



# read
map_data = read_map('map.txt')
map_size = 9



# pixel size
cell_size = window_size[0] // map_size // 4




# Initialiser une voiture
voiture_f = Voiture_F(16.75, 0.75, 0.25, 0)  # Position initiale (1, 1), vitesse 0.02, orientation Est = 1 
voiture_b = Voiture_B(voiture_f.x - cell_size, voiture_f.y - cell_size, voiture_f.vitesse, voiture_f.orientation)

# main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection des touches pour changer la direction de la voiture
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                voiture_f.orientation = 0  # Nord
                voiture_f.move()
            elif event.key == pygame.K_d:
                voiture_f.orientation = 1  # Est
                voiture_f.move()
            elif event.key == pygame.K_s:
                voiture_f.orientation = 2  # Sud
                voiture_f.move()
            elif event.key == pygame.K_a:
                voiture_f.orientation = 3  # Ouest
                voiture_f.move()
                voiture_b.x = voiture_f.x - 1.25
            elif event.key == pygame.K_g:
                if voiture_f.orientation == 0:
                    voiture_f.y -= voiture_f.vitesse
                elif voiture_f.orientation == 1:
                    voiture_f.x += voiture_f.vitesse
                elif voiture_f.orientation == 2:
                    voiture_f.y += voiture_f.vitesse
                elif voiture_f.orientation == 3:
                    voiture_f.x -= voiture_f.vitesse
            elif event.key == pygame.K_SPACE:
                voiture_f.x = 16.75
                voiture_f.y = 0.75
                voiture_f.orientation = 0

    # fill default
    window.fill((255, 255, 255))

    # draw map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # draw car
    voiture_f.draw(window, cell_size)
    voiture_b.draw(window, cell_size)
    # Refresh
    pygame.display.flip()

# Leave
pygame.quit()
