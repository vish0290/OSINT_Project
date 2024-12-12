import os
from mistralai import Mistral
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
import time
from pymongo import MongoClient
import json
import asyncio





api_key = os.environ["mistral_key"]
agent_id = os.environ["agent_id"]
db_url = os.environ["DB_URL"]
model = "open-mistral-nemo"
client = Mistral(api_key=api_key)
mongo_client = MongoClient(db_url)
db  = mongo_client.reddit
post_db = db['post_new']

rec = post_db.find()
rec = list(rec)

async def response_gen(post, agent_id):
    chat_response = await client.agents.complete(
        agent_id=agent_id,
        messages=[
            {
                "role": "user",
                "content": f"title: {post['title']}, body: {post['selftext']}",
            },
        ],
    )
    response = eval(chat_response.choices[0].message.content)
    post['response'] = response['message']
    print(f'title: {post["title"]}, response: {response["message"]}')
    await update_post(post)

async def update_post(post):
    try:
        post_db.update_one({'id':post['id']},{'$set':post},upsert=True)
        print(f'Post updated [{post["id"]}]')
    except Exception as e:
        print(e)

async def process_posts(rec, agent_id):
    tasks = [response_gen(post, agent_id) for post in rec]
    processed_count = 0

    for future in asyncio.as_completed(tasks):
        await future  # Wait for the task to complete
        processed_count += 1
        if processed_count % 100 == 0:
            print(f"Processed {processed_count} responses.")


# Run the async function
asyncio.run(process_posts(rec, agent_id))
