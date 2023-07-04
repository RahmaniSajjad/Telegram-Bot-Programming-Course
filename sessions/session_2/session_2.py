# |========> Import necessary libraries <========|
from pyrogram import Client, filters
import logging
from pysondb import db

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)

# |========> Global variables <========|
main_admin_id = 1187553221

# |========> Setup config.json <========|
ConfigAcc = db.getDb('config.json')

# Get account info from config.json
check = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})

# Keep default config
default_config = {
    'admin_list': [main_admin_id],
    'main_admin_id': main_admin_id
}

# Add account default config to config.json if it not exists
if not check:
    ConfigAcc.add(default_config)


# |========> New Message Handler <========|
@app.on_message(filters.command('phone'))
async def new_message_handler(client, message):
    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.from_user is None or message.from_user.id not in datas['admin_list']:
        await message.reply("You can't access!", quote=True)
        return

    me = await app.get_me()
    await message.reply(me.phone_number, quote=True)


@app.on_message(filters.command('id'))
async def new_message_handler(client, message):
    await message.reply(message.from_user.id, quote=True)


@app.on_message(filters.command('setAdmin'))
async def new_message_handler(client, message):
    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.reply_to_message is None:
        await message.reply("You Must Reply a Message!", quote=True)
        return

    new_id = message.reply_to_message.from_user.id
    datas['admin_list'].append(new_id)

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, datas)

    await message.reply("Done!", quote=True)


# |========> Run app <========|
app.run()
