import numpy as np
from utils import load_json
import matplotlib.pyplot as plt
import ast


def translate_map_into_prompt(map):
    # 0: empty road, 1: pedestrian, 2: forbidden pixel for the car (sidewalk), 3: our car, 4: other car
    # we want to translate this into a prompt
    context = ("Tu es un agent autonome devant agir dans un environnement. \n"
               "Tu es represente par une voiture se deplacant au sein d'une carte. \n"
               "Tu respectes les regles du code de la route francais. \n"
               "Tu peux effectuer 5 actions differentes : avancer tout droit, s'arreter, tourner a gauche, tourner a droite, reculer. \n"
               "Ta mission est d'interpreter ton environnement afin de prendre la bonne decision. \n"
               "La carte est codee sous la forme d'une matrice (liste de listes) avec des categories : \n")
    mapping = load_json()
    for key, value in mapping.items():
        context += f"{key}: {value}, \n"

    context += "La carte est la suivante : \n"
    for row in map:
        context += "[" + ", ".join(str(cell) for cell in row) + "]\n"
    context += "La direction de la voiture est indiquee grace a ses extremites avant et arriere. \n"

    question = "Que devrais-tu faire ? "
    expected_format = "Repondre sous la forme d'une action parmi les 5 actions possibles. NE RAJOUTE RIEN D'AUTRE. \n"
    return context + question + expected_format


def verify_instruct_data(data: dict):
    for example in data['messages']:
        if example['role'] == 'user':
            map = example['content'].removeprefix("La carte est la suivante : ").removesuffix(". Que devrais-tu faire ? Repondre sous la forme d'une action parmi les 5 actions possibles.")
            map = ast.literal_eval(map)

        if example['role'] == 'assistant':
            plt.title(example['content'])
            plt.imshow(map)

            for i in range(len(map)):
                for j in range(len(map[i])):
                    plt.text(j, i, str(map[i][j]), ha='center', va='center')
            plt.show()


if __name__ == "__main__":
    # map = load_map("small_map.txt")
    # prompt = translate_map_into_prompt(map)
    # print("Prompt : ", prompt)
    # answer = ask_question(prompt)
    # print("Answer : ", answer)

    data = load_json("training_data.json")
    verify_instruct_data(data)
