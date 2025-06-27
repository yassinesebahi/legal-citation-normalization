import json

input_path = "../data/normalized_citations.jsonl"
output_path = "../data/t5_tagged_training_data.jsonl"

def tag_tokens(tokens_with_labels):
    tagged_text = []
    open_tag = None

    for item in tokens_with_labels:
        token = item["token"]
        tag = item["tag"]

        if tag == "O":
            if open_tag:
                tagged_text.append(f"</{open_tag}>")
                open_tag = None
            tagged_text.append(token)
        elif tag.startswith("B-"):
            if open_tag:
                tagged_text.append(f"</{open_tag}>")
            open_tag = tag
            tagged_text.append(f"<{open_tag}>{token}")
        elif tag.startswith("I-"):
            if open_tag == tag.replace("I-", "B-"):
                tagged_text.append(f" {token}")
            else:
                # Unexpected I- tag without B-, treat as new
                if open_tag:
                    tagged_text.append(f"</{open_tag}>")
                open_tag = tag.replace("I-", "B-")
                tagged_text.append(f"<{open_tag}>{token}")
        else:
            # Unknown format, treat as O
            if open_tag:
                tagged_text.append(f"</{open_tag}>")
                open_tag = None
            tagged_text.append(token)

    if open_tag:
        tagged_text.append(f"</{open_tag}>")

    return " ".join(tagged_text)

with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
    for line in infile:
        data = json.loads(line)
        if "tags" in data and "normalized_text" in data:
            input_text = tag_tokens(data["tags"])
            target_text = data["normalized_text"]
            example = {"input": input_text, "target": target_text}
            outfile.write(json.dumps(example, ensure_ascii=False) + "\n")

print(f"Conversion complete! Output written to: {output_path}")
