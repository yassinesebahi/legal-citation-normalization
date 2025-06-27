
README for reproduction of the normalization, clustering and T5 model

Overview:
This project involves several steps for processing and normalizing legal citations from raw data. The scripts in this project handle various tasks such as cleaning raw citation data, classifying citations, tagging them with Named Entity Recognition (NER), creating training pairs for a T5 model, clustering citations using both SBERT and TF-IDF methods, and splitting the data into training, validation, and test sets.

Workflow:
The scripts are executed in sequence, with each one building upon the output of the previous step. The process starts with cleaning and classifying citations, followed by tagging, clustering, and preparing data for machine learning tasks.

The notebook ../notebooks/01 normalization.ipynb runs after script 03 and before script 04 in the following order:

---

1. 01 sort_clean_data.py: 
Purpose: This script cleans and prepares the raw citation data.
Input: Raw citation data from braces-Schleswig-Holstein-2023-06-07.txt.
Process: Removes noise from citations such as prefixes (e.g., URLs, vgl.) and extracts ECLI identifiers along with the citation text.
Output: A cleaned JSONL file (sorted_cleaned_citations.jsonl) containing the ECLI identifier and the citation text.

python 01 sort_clean_data.py

---

Note

NER tagger can be downloaded here : https://eur04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fsurfdrive.surf.nl%2Ffiles%2Findex.php%2Fs%2FFokmlNckG6M141v&data=05%7C02%7Cyassine.sebahi%40student.uva.nl%7Cebbb88a829ae46ed1b1608dd2103ee88%7Ca0f1cacd618c4403b94576fb3d6874e5%7C0%7C0%7C638703022961861275%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=MnZ%2FSkIayo3DeunG0pJsIq19WBEyQfCjpfYn9cLV1rA%3D&reserved=0


---

2. 02 classify_all.py:
Purpose: Classifies citations as either CITATION or NOT_CITATION and tags them using NER.
Input: The cleaned citation data from sorted_cleaned_citations.jsonl.
Process: Uses a classification model (classify_sentence) to label citations and NER (tag_sentence) to tag the tokens within the citations.
Output: A JSONL file (classified_citations.jsonl) containing the classification label and NER tags for each citation.

python 02 classify_all.py

---

3. 03 tag_all.py:
Purpose: Tags the CITATION entries with token-level labels using the NER model.
Input: Classified citations (classified_citations.jsonl).
Process: For each CITATION, the script applies token-level tagging using tag_sentence.
Output: A JSONL file (tagged_citations.jsonl) containing the CITATION entries with their respective tags.

python 03 tag_all.py

---

01 normalization.ipynb 
Purpose : Rule based normalization
Input : tagged_citations.jsonl

---

4. 04A clustering TF-IDF.py:
Purpose: Clusters citations using the TF-IDF and MiniBatchKMeans algorithm.
Input: Tagged citations (tagged_citations.jsonl).
Process: Uses TF-IDF to vectorize the normalized citation text and applies the MiniBatchKMeans clustering algorithm.
Output: A JSONL file (citations_with_clusters_tfidf_kmeans.jsonl) containing the citations with their assigned cluster IDs.

python 04A clustering TF-IDF.py

---

5. 04B clustering SBERT.py:
Purpose: Clusters citations using the SBERT embeddings and Agglomerative Clustering.
Input: Tagged citations (tagged_citations.jsonl).
Process: Uses the SentenceTransformer model to generate embeddings for each citation and then applies Agglomerative Clustering with cosine distance.
Output: A JSONL file (citations_with_SBERT_clusters.jsonl) containing the citations with their assigned cluster IDs.

python 04B clustering SBERT.py

---

6. 05 create_t5_pairs.py:
Purpose: Creates training data for the T5 model.
Input: Normalized citations (normalized_citations.jsonl).
Process: For each citation, it tags tokens using tag_tokens and prepares the input-output pairs for the T5 model.
Output: A JSONL file (t5_tagged_training_data.jsonl) that pairs the tokenized citation (input) with its normalized citation (target).

python 05 create_t5_pairs.py

---

7. 06 split_t5_pairs_train_validate_test.py:
Purpose: Splits the T5 training data into train, validation, and test sets.
Input: The T5 training data (t5_tagged_training_data.jsonl).
Process: Splits the dataset into training (80%), validation (10%), and test (10%) sets.
Output: A DatasetDict object containing the train, validation, and test splits.

python 06 split_t5_pairs_train_validate_test.py

---

Dependencies:
The following libraries are required to run these scripts:

sentence-transformers
sklearn
json
pandas
matplotlib
tqdm
Levenshtein
datasets

You can install the required libraries using:

pip install sentence-transformers scikit-learn pandas matplotlib tqdm Levenshtein datasets

