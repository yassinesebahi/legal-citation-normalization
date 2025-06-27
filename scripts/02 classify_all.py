import json
from label import classify_sentence, tag_sentence #put this .py file in the ner folder to run it
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

input_path = "../data/sorted_cleaned_citations.jsonl"
output_path = "../data/classified_citations.jsonl"

def process_item(item):
    citation = item.get("citation", "")
    ecli = item.get("ecli", "")
    cls_result = classify_sentence(citation)
    contains_citation = any(token["tag"] != "O" for token in cls_result)
    if contains_citation:
        label = "CITATION"
        tags = tag_sentence(citation)
    else:
        label = "NOT_CITATION"
        tags = []

    return {
        "ecli": ecli,
        "citation": citation,
        "label": label,
        "tags": tags
    }



if __name__ == "__main__":


    num_cores = cpu_count()
    print(f"Using {num_cores} CPU cores for classification...")
    with Pool(processes=num_cores) as pool:
        results = list(tqdm(pool.imap(process_item, items), total=len(items), desc="Processing test batch", mininterval=20))

    # Save test output
    with open(output_path, "w", encoding="utf-8") as outfile:
        for entry in results:
            outfile.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Test run complete. Saved to {output_path}")
