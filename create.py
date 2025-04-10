from typing import Callable
from functools import wraps

from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://goitlearn:SFcXdztN9dxbPuXa@cluster0.yygsvjh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)
db = client.book

# Decorator to handle database errors
def database_error(func: Callable) -> Callable:
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return inner

# Function to create database
@database_error
def create_db(data: list[dict]) -> list:
    result_many = db.cats.insert_many(data)
    return result_many.inserted_ids

if __name__ == "__main__":

    cats = [
        {
            "name": "Barsik",
            "age": 3,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        },
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]

    print(create_db(cats))
