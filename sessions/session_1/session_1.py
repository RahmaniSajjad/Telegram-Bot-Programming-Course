# |========> Import necessary libraries <========|
import os
from pyrogram import Client, filters
import logging
from time import time

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)

# |========> Global variables <========|
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

num1 = 1187553221  # 🟥
num2 = 1098106297  # 🟦

turn = num1


# |========> New Message Handler <========|
@app.on_message(filters.command('game'))
async def new_message_handler(client, message):
    global board
    global num1
    global num2

    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    txt = """
⬜️⬜️⬜️
⬜️⬜️⬜️
⬜️⬜️⬜️
"""

    await message.reply(txt, quote=True)


@app.on_message()
async def new_message_handler(client, message):
    global board
    global num1
    global num2
    global turn

    reply_id = message.reply_to_message_id
    if reply_id is None:
        return

    sender_id = message.from_user.id
    text = message.text

    if sender_id != turn:
        await message.reply("Not Your Turn!", quote=True)
        return

    if sender_id == num1:
        if board[int(text[0]) - 1][int(text[1]) - 1] != 0:
            await message.reply("You can't select this item!", quote=True)
            return

        board[int(text[0]) - 1][int(text[1]) - 1] = 1
        turn = num2

    elif sender_id == num2:
        if board[int(text[0]) - 1][int(text[1]) - 1] != 0:
            await message.reply("You can't select this item!", quote=True)
            return

        board[int(text[0]) - 1][int(text[1]) - 1] = 2
        turn = num1

    txt = ""

    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                txt += '⬜️'
            elif board[i][j] == 1:
                txt += '🟥'
            elif board[i][j] == 2:
                txt += '🟦'
        txt += "\n"

    await client.edit_message_text(
        chat_id=message.chat.id,
        message_id=reply_id,
        text=txt
    )

    # for i in range(3):
    #     for j in range(3):
    #         print(board[i][j], end='')
    #     print()


# |========> Run app <========

app.run()
