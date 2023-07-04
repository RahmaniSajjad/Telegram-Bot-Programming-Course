# |========> Import necessary libraries <========|
from pyrogram import Client
import logging

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)


# |========> Global variables <========|


# |========> New Message Handler <========|
@app.on_message()
async def new_message_handler(client, message):
    print(message)


# |========> Run app <========|
app.run()
