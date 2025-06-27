from datasets import load_dataset, DatasetDict

dataset = load_dataset("json", data_files="../data/t5_tagged_training_data.jsonl", split="train")
dataset = dataset.train_test_split(test_size=0.2, seed=42)

val_test = dataset["test"].train_test_split(test_size=0.5, seed=42)
dataset = DatasetDict({
    "train": dataset["train"],
    "validation": val_test["train"],
    "test": val_test["test"]
})
