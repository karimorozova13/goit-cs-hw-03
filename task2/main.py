from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient('mongodb+srv://kmoro:13091989morozova@cluster0.4wjftge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', server_api=ServerApi('1'))

db= client.cats


def add_many_cats(cats):
    try:
        if not isinstance(cats, list) or any(not isinstance(cat, dict) for cat in cats):
            raise ValueError("Input 'cats' must be a list of dictionaries")
        
        res = db.cats.insert_many(cats)
        print(f'Added {len(res.inserted_ids)} cats succesfully')
    except Exception as e:
        print(f"Error adding cats: {e}")

def add_cat(cat):
    try:
        if not isinstance(cat, dict):
            raise ValueError("Input 'cat' must be a dictionary")
        
        db.cats.insert_one(cat)
        print(f'Added cat {cat["name"]} succesfully')
    except Exception as e:
        print(f"Error adding cat: {e}")

def get_all():
    try:
        cats = db.cats.find({})
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Error retrieving cats: {e}")
        
def get_cat_by_id(id: str):
    try:
        cat = db.cats.find_one({"_id": ObjectId(id)})
        if cat:
            print(cat)
        else:
            print(f"No cat found")
    except Exception as e:
        print(f"Error retrieving cat: {e}")

def get_cat_by_name():
    try:
        name = input("Enter the cat's name, please >>>>")
        cat = db.cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"No cat found with name '{name}'")
    except Exception as e:
        print(f"Error retrieving cat: {e}")

def update_cat_age_by_name(cat_name, new_age):
    try:
        if not isinstance(cat_name, str) or not isinstance(new_age, int):
            raise ValueError("Input 'cat_name' must be a string and 'new_age' must be an integer")
        
        res =db.cats.update_one({"name": cat_name}, {"$set": {"age": new_age} })
        
        if res.modified_count > 0:
            print(f"Updated age for cat '{cat_name}' successfully")
        else:
            print(f"No cat found with name '{cat_name}'")
    except Exception as e:
        print(f"Error updating cat: {e}")
        
def add_feature(cat_name, feature):
    try:
        if not isinstance(cat_name, str) or not isinstance(feature, str):
            raise ValueError("Input 'cat_name' and 'feature' must be strings")
        
        db.cats.update_one({"name": cat_name}, {"$push": {"features": feature}})
        print(f'Cat {cat_name} was updated succesfully')
    except Exception as e:
        print(f"Error adding feature to cat: {e}")

def delete_cat(cat_name):
    try:
        if not isinstance(cat_name, str):
            raise ValueError("Input 'cat_name' must be a string")
        res = db.cats.delete_one({"name": cat_name})
        
        if res.deleted_count > 0:
            print(f"Deleted cat '{cat_name}' successfully")
        else:
            print(f"No cat found with name '{cat_name}'")
    except Exception as e:
       print(f"Error deleting cat: {e}")

def delete_all_cats():
    try:
        res = db.cats.delete_many({})
        print(f"Deleted {res.deleted_count} cats successfully")
    except Exception as e:
        print(f"Error deleting cats: {e}")



    """ You can add cats just in such format:
{
    "_id": ObjectId("60d24b783733b1ae668d4a77"),
    "name": "barsik",
    "age": 3,
    "features": ["ходить в капці", "дає себе гладити", "рудий"]
}
    """

cats =[
        {
            "name": "Poly",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Ajax",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
        {
            "name": 'Lilu',
            "age": 13,
            "features": ["ходить в капці", "дає себе гладити", "рудий"],
        }
    ]

add_many_cats(cats)
print('\n')
add_cat({
            "name": "Kari",
            "age": 13,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },)
print('\n')
get_all()
print('\n')
get_cat_by_id("6617af3cc5efccd85c7db825")
print('\n')
get_cat_by_name()
print('\n')
update_cat_age_by_name('Lilu',7)
print('\n')
add_feature('Kari', 'amazing')
print('\n')
delete_cat('Ajax')
print('\n')
delete_all_cats()

