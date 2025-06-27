import json
from label import tag_sentence
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

input_path = "../data/classified_citations.jsonl"
output_path = "../data/tagged_citations.jsonl"

with open(input_path, "r", encoding="utf-8") as infile:
    citation_entries = [json.loads(line) for line in infile if '"CITATION"' in line]

def process_entry(entry):
    entry["tags"] = tag_sentence(entry["citation"])
    return entry

if __name__ == "__main__":
    print(f"Using {num_cores} CPU cores for tagging...")

    with Pool(processes=8) as pool:
        updated_entries = list(tqdm(pool.imap(process_entry, citation_entries), total=len(citation_entries), desc="Re-tagging citations"))

    with open(output_path, "w", encoding="utf-8") as outfile:
        for entry in updated_entries:
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Saved all 'CITATION' entries with their tags to {output_path}")
