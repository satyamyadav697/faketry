import random
from pyrogram import enums, filters
from Oneforall import app

random_photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

INFO_TEXT = """<b>
❅─────✧❅✦❅✧─────❅
✦ USER INFO ✦

➻ USER ID ‣</b> <code>{}</code>
<b>➻ FIRST NAME ‣</b> {}
<b>➻ LAST NAME ‣</b> {}
<b>➻ USERNAME ‣</b> {}
<b>➻ MENTION ‣</b> {}
<b>➻ LAST SEEN ‣</b> {}
<b>➻ DC ID ‣</b> {}
<b>➻ BIO ‣</b> {}

❅─────✧❅✦❅✧─────❅
"""

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        status = user.status
        if status == enums.UserStatus.RECENTLY:
            return "Recently"
        elif status == enums.UserStatus.LAST_WEEK:
            return "Last week"
        elif status == enums.UserStatus.LONG_AGO:
            return "Long time ago"
        elif status == enums.UserStatus.OFFLINE:
            return "Offline"
        elif status == enums.UserStatus.ONLINE:
            return "Online"
    except:
        return "Something went wrong"

@app.on_message(filters.command(["info", "userinfo"]))
async def userinfo(_, message):
    chat_id = message.chat.id
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        elif len(message.command) > 1:
            user = await app.get_users(message.command[1])
        else:
            user = message.from_user

        user_info = await app.get_chat(user.id)
        status = await userstatus(user.id)

        id = user_info.id
        dc_id = user.dc_id
        first_name = user_info.first_name
        last_name = user_info.last_name or "No last name"
        username = f"@{user_info.username}" if user_info.username else "No username"
        mention = user.mention
        bio = user_info.bio or "No bio set"

        photo = random.choice(random_photo)

        await app.send_photo(
            chat_id,
            photo=photo,
            caption=INFO_TEXT.format(id, first_name, last_name, username, mention, status, dc_id, bio),
            reply_to_message_id=message.id,
            parse_mode="html",
        )

    except Exception as e:
        await message.reply_text(f"<b>Error:</b> <code>{str(e)}</code>", parse_mode="html")
