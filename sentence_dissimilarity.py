import numpy as np
import json
import math

# Load entity level dissimilarity matrix
with open("entity_dissimilarity.json", "r") as f:
    dissimilarity_matrix = json.load(f)


# Get sentence level dissimilarity score
def sentence_dissimilarity(entities_a, entities_b, default_dissim=1.0):

    # Edge cases
    if not entities_a:
        return 0.0
    if not entities_b:
        return default_dissim

    total = 0.0

    for ea in entities_a:
        min_d = math.inf

        for eb in entities_b:
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
def compute_symmetric_dissimilarity_matrix(entities_per_sentence):
    n = len(entities_per_sentence)
    matrix = np.zeros((n, n))

    for i in range(n):
        matrix[i][i] = 0  # explicitly set diagonal to zero
        for j in range(i + 1, n):  # only upper triangle (excluding diagonal)
            score = sentence_dissimilarity(
                entities_per_sentence[i],
                entities_per_sentence[j]
            )
            matrix[i][j] = score
            matrix[j][i] = score  # mirror to lower triangle

    return matrix