from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import json
from tqdm import tqdm

with open("../data/normalized_citations.jsonl", "r", encoding="utf-8") as f:
    citations = [json.loads(line) for line in f]


texts = [c["normalized_text"] for c in citations]
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

clustering = AgglomerativeClustering(
    n_clusters=None,
    distance_threshold=0.3,
    metric="cosine",
    linkage="average"
)
labels = clustering.fit_predict(embeddings)

for citation, label in zip(citations, labels):
    citation["cluster_id"] = int(label)

with open("../data/citations_with_SBERT_clusters.jsonl", "w", encoding="utf-8") as f:
    for c in citations:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
