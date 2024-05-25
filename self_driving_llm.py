import numpy as np


def translate_map_into_prompt(map: np.ndarray):
    # 0: empty road, 1: pedestrian, 2: forbidden pixel for the car (sidewalk), 3: our car, 4: other car
    # we want to translate this into a prompt
    context = ("Tu es un agent autonome devant agir dans un environnement. "
               "Tu es représenté par une voiture se déplaçant au sein d'une carte. "
               "Tu respectes les règles du code de la route français. "
               "Tu peux effectuer 5 actions différentes : avancer tout droit, s'arrêter, tourner à gauche, tourner à droite, reculer. "
               "Ta mission est d'interpréter ton environnement afin de prendre la bonne décision. "
               "La carte est codée sous la forme d'une matrice avec 20 catégories différentes : 3 : Panneau de signalisation de danger (triangle), 4 : Feu rouge, 5 : Feu orange, 6 : Feu vert, 7 : Panneau de priorité à droite (rond avec une flèche vers la droite), 8 : Panneau de cédez-le-passage (triangle avec une ligne horizontale), 9 : Panneau de stop (octogone avec le mot 'STOP' écrit en blanc sur fond rouge), 10 : Panneau de sens interdit (rond avec une ligne horizontale barrée), 11 : Panneau de limitation de vitesse (rond avec un chiffre indiquant la vitesse maximale autorisée), 12 : Panneau de fin de limitation de vitesse (rond avec une ligne horizontale barrée et un chiffre indiquant la vitesse maximale autorisée), 13 : Panneau de passage piéton (rectangle avec deux personnages marchant), 14 : Panneau de signalisation de travaux (triangle avec une image de travaux), 15 : Panneau de signalisation de chaussée glissante (triangle avec une image de chaussée glissante), 16 : Panneau de signalisation de virage dangereux (triangle avec une image de virage), 17 : Panneau de signalisation de traversée d'animaux (triangle avec une image d'animaux), 18 : Panneau de signalisation de passage à niveau (triangle avec une image de passage à niveau), 19 : Panneau de signalisation de stationnement interdit (rectangle avec une image de voiture barrée), 20 : Panneau de signalisation de stationnement autorisé (rectangle avec une image de voiture et une flèche): \n")
    context += "La carte est la suivante : \n"
    for row in map:
        context += " ".join(str(cell) for cell in row) + "\n"
    return context

