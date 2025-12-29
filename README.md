# Ontology-based Semantic Clustering

<img src="image.png"/>
<img src="image1.png"/>

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/RaoGhulam/semantic_clustering.git
cd semantic_clustering
```

### 2. Create and activate a virtual environment (optional but recommended)
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Linux/macOS
source venv/bin/activate

# Windows
# venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
---

## Methodology
1. **Entity Extraction**
Sentences are first processed using **POS tagging** from NLTK to identify potential entities.

2. **Entity Linking**
Extracted entities are linked to real entities in the ontology. This step uses **fuzzy matching** and **synonyms** to handle variations in wording and ensure correct alignment with the ontology.

3. **Entity-to-Entity Dissimilarity**
For any two sentences, a **precomputed entity-to-entity dissimilarity matrix** is used to calculate the dissimilarity score between each entity in the first sentence and each entity in the second sentence.  
**Note:** The entity-to-entity dissimilarity score is calculated using the method proposed by D. Sánchez et al., ***“Ontology-based semantic similarity: A new feature-based approach”, Expert Systems with Applications,*** 2012 (Elsevier).  
For more details, refer to the [**Taxonomy-based Feature Dissimilarity Measure** PDF](taxonomy_based_feature_dissimilarity_measure.pdf).

5. **Sentence-Level Dissimilarity**
The entity-to-entity dissimilarity scores are then **aggregated** to obtain a **sentence-to-sentence dissimilarity score**, providing a semantic measure of how similar two sentences are based on their underlying entities.  
These scores are stored in a **NumPy matrix** called `sentence_dissimilarity_matrix`.
For more details, refer to the [**Taxonomy-based Feature Dissimilarity Measure** PDF](taxonomy_based_feature_dissimilarity_measure.pdf).

6. **Clustering Sentences**  
   - Apply **Agglomerative Hierarchical Clustering** using **average linkage**, with the sentence dissimilarity matrix as the distance metric.  
   - Compute the **Silhouette score** to determine the **optimal number of clusters**.  
   - Using the optimal number of clusters, create a **clustered set of sentences**, where semantically similar sentences are grouped together.
