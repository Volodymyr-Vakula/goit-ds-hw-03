import json
from create import client

# Function to load data from a json file
def load_from_json_file(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

db = client.books

try:
    db.quotes.insert_many(load_from_json_file("quotes.json"))
    db.authors.insert_many(load_from_json_file("authors.json"))
except Exception as e:
    print(f"Error: {e}")
