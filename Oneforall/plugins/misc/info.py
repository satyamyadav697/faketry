from pyrogram import Client, filters, enums
from Oneforall import app

INFO_TEXT = """**
❅─────✧❅✦❅✧─────❅
            ✦ ᴜsᴇʀ ɪɴғᴏ ✦

➻ ᴜsᴇʀ ɪᴅ ‣ **`{}`
**➻ ғɪʀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ʟᴀsᴛ ɴᴀᴍᴇ ‣ **{}
**➻ ᴜsᴇʀɴᴀᴍᴇ ‣ **`{}`
**➻ ᴍᴇɴᴛɪᴏɴ ‣ **{}
**➻ ʟᴀsᴛ sᴇᴇɴ ‣ **{}
**➻ ᴅᴄ ɪᴅ ‣ **{}
**➻ ʙɪᴏ ‣ **`{}`

**❅─────✧❅✦❅✧─────❅**
"""

async def userstatus(user):
    try:
        if user.status == enums.UserStatus.RECENTLY:
            return "Recently"
        elif user.status == enums.UserStatus.LAST_WEEK:
            return "Last week"
        elif user.status == enums.UserStatus.LONG_AGO:
            return "Long time ago"
        elif user.status == enums.UserStatus.OFFLINE:
            return "Offline"
        elif user.status == enums.UserStatus.ONLINE:
            return "Online"
        else:
            return "Unknown"
    except:
        return "Couldn't fetch"

@app.on_message(filters.command(["info", "userinfo"]))
async def userinfo(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    user_info = await client.get_chat(user.id)
    status = await userstatus(user)

    user_id = user_info.id
    first_name = user_info.first_name
    last_name = user_info.last_name or "No last name"
    username = user_info.username or "No username"
    mention = user.mention
    dc_id = user_info.dc_id or "Unknown"
    bio = user_info.bio or "No bio set"

    text = INFO_TEXT.format(user_id, first_name, last_name, username, mention, status, dc_id, bio)

    await message.reply(text, parse_mode="markdown")
