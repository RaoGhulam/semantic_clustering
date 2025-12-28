from get_entities import get_entities
import numpy as np
import json
import math

# Load ontology file
ontology_file = r"E:\Practice\krr\KRR_Project\new_islam_ontology_tur.ttl"

# Load dissimilarity matrix
with open("entity_dissimilarity.json", "r") as f:
    dissimilarity_matrix = json.load(f)


# Get sentence level dissimilarity
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

# ---------------- Example ----------------
if __name__ == "__main__":
    s1 = "I performed Fajar, Zuhr, and Bright Moon Fasting today.During Hajj, I visited Mina and performed Tawaf."

    s2 = "The individual performed Fajr and Zuhr prayers and observed Bright Moon fasting. During Hajj, Mina was visited and Tawaf was completed."
    
    score = sentence_dissimilarity(s1, s2)
    print(score)
