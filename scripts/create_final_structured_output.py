import json
from pathlib import Path

# Load the clustered SBERT citations
with open("../data/citations_with_SBERT_clusters.jsonl", "r", encoding="utf-8") as f:
    citations = [json.loads(line) for line in f]

# Define relevant German metadata fields to extract from normalized_fields
metadata_keys = [
    "Gericht", "Datum", "Aktenzeichen", "Seite-Beginn", "Randnummer", "Zeitschrift",
    "Jahr", "Autor", "Paragraph", "Gesetz", "Seite-Fundstelle", "Nummer", "Auflage",
    "Titel", "Editor", "Wort:aaO", "Wort:Auflage"
]

# Build the structured output
structured_output = []
for entry in citations:
    metadata = {}
    fields = entry.get("normalized_fields", {})
    for key in metadata_keys:
        if key in fields:
            metadata[key] = fields[key]

    structured_output.append({
        "ecli": entry.get("ecli"),
        "original_text": entry.get("citation"),
        "normalized_text": entry.get("normalized_text"),
        "id": entry.get("id"),
        "citation_type": entry.get("citation_type"),
        "cluster_id": entry.get("cluster_id_sbert"),
        "metadata": metadata,
    })

# Save to JSONL
output_path = "../data/final_structured_citations.jsonl"
with open(output_path, "w", encoding="utf-8") as f:
    for record in structured_output:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

output_path
