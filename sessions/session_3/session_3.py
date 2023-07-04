# |========> Import necessary libraries <========|
from pyrogram import Client, filters, errors
from pyrogram.enums import ChatType
import logging
import asyncio
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)

# |========> Global variables <========|

text = "test!"

chat_id = 0

# |========> Setup scheduler <========|
asia_tehran = pytz.timezone('Asia/Tehran')
scheduler = AsyncIOScheduler(timezone=asia_tehran)
scheduler.start()


# |========> New Message Handler <========|
@app.on_message(filters.command('text'))
async def new_message_handler(client, message):
    global text

    text = message.reply_to_message.text

    await message.reply("Done!")


@app.on_message(filters.command('stop'))
async def new_message_handler(client, message):

    this_job = scheduler.get_job(job_id="timer")
    if this_job is not None:
        scheduler.remove_job(job_id="timer")
        await message.reply("Stopped!")
    else:
        await message.reply("Already Not Exist!")


@app.on_message(filters.command('do'))
async def new_message_handler(client, message):
    global text
    global chat_id

    chat_id = message.chat.id

    sleep_time = int(message.text.split()[1])

    this_job = scheduler.get_job(job_id="timer")
    if this_job is None:
        scheduler.add_job(timer_job, "interval", seconds=sleep_time, id="timer")
        await message.reply("Ruined!")
    else:
        await message.reply("Already Exist!")


async def timer_job():
    global chat_id

    await app.send_message(chat_id=chat_id, text=text)


# |========> Run app <========|
app.run()
