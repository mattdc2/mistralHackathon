import numpy as np
# from mistral_api import ask_question
from mistral_model import ask_question
from utils import load_mapping, load_map


def translate_map_into_prompt(map: np.ndarray):
    # 0: empty road, 1: pedestrian, 2: forbidden pixel for the car (sidewalk), 3: our car, 4: other car
    # we want to translate this into a prompt
    context = ("Tu es un agent autonome devant agir dans un environnement. \n"
               "Tu es represente par une voiture se deplacant au sein d'une carte. \n"
               "Tu respectes les regles du code de la route francais. \n"
               "Tu peux effectuer 5 actions differentes : avancer tout droit, s'arreter, tourner a gauche, tourner a droite, reculer. \n"
               "Ta mission est d'interpreter ton environnement afin de prendre la bonne decision. \n"
               "La carte est codee sous la forme d'une matrice (liste de listes) avec des categories : \n")
    mapping = load_mapping()
    for key, value in mapping.items():
        context += f"{key}: {value}, \n"

    context += "La carte est la suivante : \n"
    for row in map:
        context += "[" + ", ".join(str(cell) for cell in row) + "]\n"

    question = "Que devrais-tu faire ? "
    expected_format = "Répondre sous la forme d'une action parmi les 5 actions possibles."
    return context + question + expected_format


if __name__ == "__main__":
    map = load_map("small_map.txt")
    prompt = translate_map_into_prompt(map)
    print("Prompt : ", prompt)
    answer = ask_question(prompt)
    print("Answer : ", answer)

