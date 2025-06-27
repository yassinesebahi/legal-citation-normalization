import re
import json
from pathlib import Path

input_file = Path("../data/braces-data/braces-Schleswig-Holstein-2023-06-07.txt")
output_file = Path("../data/sorted_cleaned_citations.jsonl")

citation_clean_pattern = re.compile(r"^(?:\.\./[^ ]*|vgl\.|https?://\S+)\s*")
ecli_prefix = "../../gesp-experiments/unified-gesp-dataset/"

records = []

with input_file.open("r", encoding="utf-8", errors="replace") as f:
    for line in f:
        line = line.strip()
        if line.startswith(ecli_prefix):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                path_part, citation_part = parts
                ecli = path_part.split("/")[-1]
                cleaned_citation = re.sub(citation_clean_pattern, '', citation_part)
                records.append({
                    "ecli": ecli,
                    "citation": cleaned_citation
                })

with output_file.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

print(f"Done {len(records)} citations saved to {output_file}")
