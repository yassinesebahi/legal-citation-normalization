import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from pathlib import Path
from tqdm import tqdm


input_path = "../data/normalized_citations.jsonl"
with open(input_path, "r", encoding="utf-8") as f:
    citations = [json.loads(line) for line in f]

texts = [c["normalized_text"] for c in citations]

vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_df=0.8, min_df=2)
X = vectorizer.fit_transform(texts)


n_clusters = 300 
kmeans = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1024, max_iter=300)
print("Clustering with MiniBatchKMeans...")
clusters = list(tqdm(kmeans.fit_predict(X), total=len(citations)))

for citation, cluster_id in zip(citations, clusters):
    citation["cluster_id_tfidf_kmeans"] = int(cluster_id)


output_path = "../data/citations_with_clusters_tfidf_kmeans.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for citation in citations:
        json.dump(citation, f, ensure_ascii=False)
        f.write("\n")

print(f"TF-IDF clustering with MiniBatchKMeans complete. Saved to: {output_path}")


