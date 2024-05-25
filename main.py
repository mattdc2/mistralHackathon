import pygame
import time






# parser
def read_map(filename):
    with open(filename, 'r') as file:
        map_data = []
        for line in file:
            row = list(map(int, line.split()))
            map_data.append(row)
    return map_data










# Classe Voiture
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
        # Dessiner la voiture comme un rectangle rouge
        if self.orientation == 0 or self.orientation == 2:
            car_width = cell_size
            car_len = car_width * 2
        elif self.orientation == 1 or self.orientation == 3:
            car_len = cell_size
            car_width = car_len * 2
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)







# Init
pygame.init()

# window init
window_size = (1200, 1200)
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
map_size = 10



# pixel size
cell_size = window_size[0] // map_size // 4




# Initialiser une voiture
voiture = Voiture(1, 1, 1, 1)  # Position initiale (1, 1), vitesse 0.02, orientation Est = 1 


# main
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection des touches pour changer la direction de la voiture
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                voiture.orientation = 0  # Nord
                voiture.move()
            elif event.key == pygame.K_d:
                voiture.orientation = 1  # Est
                voiture.move()
            elif event.key == pygame.K_s:
                voiture.orientation = 2  # Sud
                voiture.move()
            elif event.key == pygame.K_a:
                voiture.orientation = 3  # Ouest
                voiture.move()

    # fill default
    window.fill((255, 255, 255))

    # draw map
    for row in range(len(map_data)):
        for col in range(len(map_data[row])):
            value = map_data[row][col]
            color = colors.get(value, (0, 0, 0))  # Par défaut noir si valeur non trouvée
            pygame.draw.rect(window, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Mettre à jour la position de la voiture
    # voiture.move()

    # draw car
    voiture.draw(window, cell_size)

    # Refresh
    pygame.display.flip()

# Leave
pygame.quit()
