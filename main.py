from create import database_error, db

# Function to read all data in collection
@database_error
def read_all_data() -> list[dict]:
    result = db.cats.find({})
    all_data = []
    for el in result:
        all_data.append(el)
    return all_data

# Function to read data related to cat's name
@database_error
def read_data_by_name(name: str) -> dict:
    result = db.cats.find_one({"name": name})
    return result

# Function to update age by cat's name
@database_error
def update_age_by_name(name: str, age: int) -> dict:
    db.cats.update_one({"name": name}, {"$set": {"age": age}})
    return read_data_by_name(name)

# Function to add new feature by cat's name
@database_error
def add_feature_by_name(name: str, feature: str) -> dict:
    db.cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
    return read_data_by_name(name)

# Function to delete data by cat's name
@database_error
def delete_by_name(name: str) -> dict|None:
    db.cats.delete_one({"name": name})
    return read_data_by_name(name)

# Function to delete all data from collection
@database_error
def delete_all_data() -> None:
    result = db.cats.find({})
    for el in result:
        delete_by_name(el["name"])

if __name__ == "__main__":

    # print(add_feature_by_name("Barsik", "crazy"))
    # print(read_all_data())
    # print(delete_by_name("barsik"))
    # delete_all_data()
    # read_all_data()
    print(update_age_by_name("Barsik", 7))
    # delete_all_data()
