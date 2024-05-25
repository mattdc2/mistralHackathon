import pygame
import random
import time


############################# MAP PARSER + TESTS ############################

def read_map(filename):
    with open(filename, 'r') as file:
        map_data = []
        for line in file:
            row = list(map(int, line.split()))
            map_data.append(row)
    return map_data

# return liste of random int between 0 and 5 (to remove)
def random_inputs():
    input_liste = []
    for _ in range(10):
        input_random = random.randint(0, 5)
        input_liste.append(input_random)
    print(input_liste)
    return input_liste

############################# FRONT CAR CLASS ############################

class Voiture_F:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest

    # move the car with WASD
    def keyboard_move(self):
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

    # draw the front of the car (red square)
    def draw(self, window, cell_size):
        car_width = cell_size
        car_len = cell_size
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (255, 0, 0), car_rect)

    # move the car with the 5 case that LLM is returning 
    def interpreter(self, retour):
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
            self.y += 1
            self.x = self.x
        if retour == 2:
            self.y -= 1
            self.x = self.x
        if retour == 3:
            self.x += 1
            self.y = self.y
        if retour == 4:
            self.x -= 1
            self.y = self.y
            
############################ BACK CAR CLASS ############################

class Voiture_B:
    def __init__(self, x, y, vitesse, orientation):
        self.x = x
        self.y = y
        self.vitesse = vitesse
        self.orientation = orientation  # 0: Nord, 1: Est, 2: Sud, 3: Ouest

    # keyboard_kemovemove the car with WASD (can be optimized it's always the same moove, the B one take the place of the A one)
    def keyboard_move(self):
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
    
    # draw the back of the car (green square)
    def draw(self, window, cell_size):    
        car_width = cell_size
        car_len = cell_size
        car_rect = pygame.Rect(self.x * cell_size + cell_size // 4, self.y * cell_size + cell_size // 4, car_width, car_len)
        pygame.draw.rect(window, (0, 255, 0), car_rect)

############################# INIT ############################

# game init
pygame.init()

# window init
window_size = (1620, 1080)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simulation de Ville")

# color structure
colors = {
    0: (0, 0, 0),        # Noir (route)
    1: (255, 255, 255),  # Blanc (autre)
    2: (0, 0, 255),        # panneaux
    3: (100, 130, 110),   # Border
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

random_inputs() # debug

############################# MAIN LOOP ############################

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Détection des touches pour changer la direction de la voiture
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                voiture_f.orientation = 0  # Nord
                voiture_b.keyboard_move()
                voiture_f.keyboard_move()
            elif event.key == pygame.K_a:
                voiture_f.orientation = 1  # Est
                voiture_b.keyboard_move()
                voiture_f.keyboard_move()
            elif event.key == pygame.K_w:
                voiture_f.orientation = 2  # Sud
                voiture_b.keyboard_move()
                voiture_f.keyboard_move()
            elif event.key == pygame.K_d:
                voiture_f.orientation = 3  # Ouest
                voiture_b.keyboard_move()
                voiture_f.keyboard_move()
            elif event.key == pygame.K_SPACE:
                voiture_f.x = 16.75
                voiture_f.y = 0.75
                voiture_b.x = 16.75
                voiture_b.y = 0.75 - 1
                voiture_f.orientation = 0
            # l binded to run random input tests
            elif event.key == pygame.K_l:
                new_liste = random_inputs()
                for nombre in new_liste:
                    voiture_b.interpreteur(nombre)
                    voiture_f.interpreter(nombre)
                    print(nombre) #debug
            elif event.key == pygame.K_ESCAPE:
                running = False

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
