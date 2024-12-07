import time
import httpx
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

def mongo_connect():
    db_url = os.getenv("DB_URL")
    try:
        client = MongoClient(f"")
        db = client.reddit
        post_db = db['post']
        comment_db = db['comment']
        return post_db, comment_db
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")
        
def upload_to_mongo(df,db):
    try:
        records = df.to_dict(orient='records')
        db.insert_many(records)
        print("Data uploaded to MongoDB")
    except Exception as e:
        print(f"Error uploading data to MongoDB: {str(e)}")

def get10rec(post_db):
    try:
        return post_db.find().limit(10)
    except Exception as e:
        print(f"Error fetching data from MongoDB: {str(e)}")
    

base_url = "https://www.reddit.com"
endpoint = "/r/startups"
category = "/new"

url = base_url + endpoint + category + ".json"
after_post_id = None

# dataset = []
post_db, comment_db = mongo_connect()


for i in range(2):
    params = {
        'limit': 100,
        't':'all',
        'after': after_post_id
    }
    response = httpx.get(url, params=params)
    print(f"Request {i+1} - Status code: {response.status_code}")
    if response.status_code != 200:
        raise Exception("Failed to fetch data")
    
    json_data = response.json()
    df = pd.DataFrame(json_data['data']['children'])
    upload_to_mongo(df, post_db)
    after_post_id = json_data['data']['after']
    time.sleep(2)

# res = get10rec(post_db)
# print(res[0]['data']['title']) 
