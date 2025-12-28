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

## Semantic Clustering vs Traditional Clustering

Traditional clustering methods (like K-Means or hierarchical clustering using bag-of-words or TF-IDF) group data based on surface-level similarities—i.e., the exact words or features that appear in the sentences. If two sentences use different words, they may be considered completely different, even if they mean the same thing.

Semantic clustering, on the other hand, groups sentences based on meaning rather than exact wording.
Example:

""I performed Fajar, Zuhr, and Bright Moon Fasting today. During Hajj, I visited Mina and performed Tawaf."

"I performed the Islamic morning prayer, noon salah, and observed Ayyamul Beed fasting today. During the mandatory Islamic pilgrimage, I visited the Mina Valley and performed Namaz-e-Tawaf."

Traditional clustering might treat these as different, but semantic clustering recognizes their semantic similarity and groups them together.

## Methodology
1. **Entity Extraction**
Sentences are first processed using **POS tagging** from NLTK to identify potential entities.

2. **Entity Linking**
Extracted entities are linked to real entities in the ontology. This step uses **fuzzy matching** and **synonyms** to handle variations in wording and ensure correct alignment with the ontology.

3. **Entity-to-Entity Dissimilarity**
For any two sentences, a **precomputed entity-to-entity dissimilarity matrix** is used to calculate the dissimilarity score between each entity in the first sentence and each entity in the second sentence.  
**Note:** This method is based on the work by D. Sánchez et al., ***“Ontology-based semantic similarity: A new feature-based approach”, Expert Systems with Applications,*** 2012 (Elsevier).  
For more details, refer to the [**Taxonomy-based Feature Dissimilarity Measure** PDF](taxonomy_based_feature_dissimilarity_measure.pdf).

5. **Sentence-Level Dissimilarity**
The entity-to-entity dissimilarity scores are then **aggregated** to obtain a **sentence-to-sentence dissimilarity score**, providing a semantic measure of how similar two sentences are based on their underlying entities.  
These scores are stored in a **NumPy matrix** called `sentence_dissimilarity_matrix`.
For more details, refer to the [**Taxonomy-based Feature Dissimilarity Measure** PDF](taxonomy_based_feature_dissimilarity_measure.pdf).

6. **Clustering Sentences**  
   - Apply **Agglomerative Hierarchical Clustering** using **average linkage**, with the sentence dissimilarity matrix as the distance metric.  
   - Compute the **Silhouette score** to determine the **optimal number of clusters**.  
   - Using the optimal number of clusters, create a **clustered set of sentences**, where semantically similar sentences are grouped together.
