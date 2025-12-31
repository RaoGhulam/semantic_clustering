from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
from ontology_sentence_dissimilarity import ontology_sentence_dissimilarity_matrix
from neural_sentence_dissimilarity import neural_sentence_dissimilarity_matrix
from collections import defaultdict
from sklearn.metrics import silhouette_score

def cluster_sentences(sentences, clustering_method, max_clusters=10):

    # Step 1: Compute the symmetric dissimilarity matrix based on clustering_method
    if clustering_method == "ontology":
        dissimilarity_matrix = ontology_sentence_dissimilarity_matrix(sentences)

    elif clustering_method ==  "neural":
        dissimilarity_matrix = neural_sentence_dissimilarity_matrix(sentences)

    else:
        print("Error")
    
    # Step 2: Find optimal number of clusters using silhouette score
    best_n = 2
    best_score = -1
    max_test_clusters = min(len(sentences) - 1, max_clusters)

    for n in range(2, max_test_clusters + 1):
        clustering = AgglomerativeClustering(
            n_clusters=n,
            metric='precomputed',
            linkage='average'
        )
        labels = clustering.fit_predict(dissimilarity_matrix)
        score = silhouette_score(dissimilarity_matrix, labels, metric='precomputed')
        if score > best_score:
            best_score = score
            best_n = n

    # Step 3: Cluster sentences using the optimal number of clusters
    clustering = AgglomerativeClustering(
        n_clusters=best_n,
        metric='precomputed',
        linkage='average'
    )
    labels = clustering.fit_predict(dissimilarity_matrix)

    # Step 4: Group sentences by cluster
    clusters = defaultdict(list)
    for sentence, label in zip(sentences, labels):
        clusters[label].append(sentence)

    # Optional: visualize dendrogram
    # if visualize:
    #     condensed_dist = squareform(dissimilarity_matrix)
    #     Z = linkage(condensed_dist, method='average')
    #     plt.figure(figsize=(10, 5))
    #     dendrogram(Z, labels=[f"Sent {i}" for i in range(len(sentences))])
    #     plt.title(f"Hierarchical Clustering Dendrogram (Optimal clusters: {best_n})")
    #     plt.show()

    return clusters, best_n


# ------------------------Standalone usage------------------------
if __name__ == "__main__":
    example_sentences = [
        "I performed Fajr, Zuhr, and Bright Moon fasting today at Masjid al-Haraam.",
        "During Hajj, I visited Mina and performed Tawaff prayer around Mataf.",
        "I observed Ramadan fasting and offered Asar and Maghrib prayers.",
        "Today, I gave Zakat al-Maal to eligible people through Amil and Distribution channels."
    ]

    clustered, optimal_n = cluster_sentences(example_sentences, visualize=True)
    print(f"\nOptimal number of clusters: {optimal_n}")
    for label, cluster_sents in clustered.items():
        print(f"\nCluster {label}:")
        for s in cluster_sents:
            print(f" - {s}")