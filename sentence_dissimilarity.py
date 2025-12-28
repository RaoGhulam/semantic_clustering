from get_entities import get_entities
import numpy as np
import json
import math
import os

# Load ontology file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ontology_file = os.path.join(BASE_DIR, "new_islam_ontology_tur.ttl")

# Load entity level dissimilarity matrix
with open("entity_dissimilarity.json", "r") as f:
    dissimilarity_matrix = json.load(f)


# Get sentence level dissimilarity score
def sentence_dissimilarity(sent_a, sent_b, default_dissim=1.0):
    entities_a = get_entities(sent_a, ontology_file)
    entities_b = get_entities(sent_b, ontology_file)

    # Edge cases
    if not entities_a:
        return 0.0
    if not entities_b:
        return default_dissim

    total = 0.0

    for ea in entities_a:
        min_d = math.inf

        for eb in entities_b:
            # SAFE lookup: do NOT use `or`
            if ea in dissimilarity_matrix and eb in dissimilarity_matrix[ea]:
                d = dissimilarity_matrix[ea][eb]
            elif eb in dissimilarity_matrix and ea in dissimilarity_matrix[eb]:
                d = dissimilarity_matrix[eb][ea]
            else:
                d = default_dissim

            min_d = min(min_d, d)

        total += min_d

    return total / len(entities_a)


# Sentence Level Dissimilarity Matrix
def compute_symmetric_dissimilarity_matrix(sentences):
    n = len(sentences)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i, n):  # only compute upper triangle including diagonal
            score = sentence_dissimilarity(sentences[i], sentences[j])
            matrix[i][j] = score
            matrix[j][i] = score  # mirror to lower triangle
    
    return matrix

# ------------------------Standalone usage------------------------
if __name__ == "__main__":

    try:
        option = int(input(
            "1) Test Sentence dissimilarity score\n"
            "2) Test Sentence dissimilarity matrix\n"
            "Select the option: "
        ))

        if option == 1:
            s1 = (
                "I performed Fajar, Zuhr, and Bright Moon Fasting today. "
                "During Hajj, I visited Mina and performed Tawaf."
            )
            s2 = (
                "I performed the Islamic morning prayer, noon salah, and observed "
                "Ayyamul Beed fasting today. During the mandatory Islamic pilgrimage, "
                "I visited the Mina Valley and performed Namaz-e-Tawaf."
            )
            score = sentence_dissimilarity(s1, s2)
            print(f"Dissimilarity score: {score}")

        elif option == 2:
            sentences = [
                "I performed Fajr, Zuhr, and Bright Moon fasting today at Masjid al-Haraam.",
                "During Hajj, I visited Mina and performed Tawaff prayer around Mataf.",
                "The individual observed Ramadan fasting and offered Asar and Maghrib prayers.",
                "Today, I gave Zakat al-Maal to eligible people through Amil and Distribution channels.",
                "I attended Eid prayer and performed Tahajud prayer in the early morning."
            ]
            print(
                "Dissimilarity Matrix:\n",
                compute_symmetric_dissimilarity_matrix(sentences)
            )

        else:
            print("Invalid option. Please select 1 or 2.")

    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
