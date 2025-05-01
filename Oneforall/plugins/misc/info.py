from pyrogram import enums, filters
from Oneforall import app

INFO_TEXT = """
<b>❅─────✧❅✦❅✧─────❅</b>
<b>✦ USER INFO ✦</b>

➻ <b>USER ID:</b> <code>{}</code>
➻ <b>FIRST NAME:</b> {}
➻ <b>LAST NAME:</b> {}
➻ <b>USERNAME:</b> <code>{}</code>
➻ <b>MENTION:</b> {}
➻ <b>LAST SEEN:</b> {}
➻ <b>DC ID:</b> {}
➻ <b>BIO:</b> <code>{}</code>

<b>❅─────✧❅✦❅✧─────❅</b>
"""

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        status = user.status
        return {
            enums.UserStatus.RECENTLY: "Recently",
            enums.UserStatus.LAST_WEEK: "Last week",
            enums.UserStatus.LONG_AGO: "Long time ago",
            enums.UserStatus.OFFLINE: "Offline",
            enums.UserStatus.ONLINE: "Online"
        }.get(status, "Unknown")
    except:
        return "Something went wrong!"

@app.on_message(filters.command(["info", "userinfo"], prefixes=["/", "!", ".", "#"]))
async def userinfo(_, message):
    try:
        user = None
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        elif len(message.command) == 2:
            user = await app.get_users(message.command[1])
        else:
            user = message.from_user

        user_info = await app.get_chat(user.id)
        status = await userstatus(user.id)
        id = user.id
        dc_id = user.dc_id
        first_name = user.first_name or "No first name"
        last_name = user.last_name or "No last name"
        username = user.username or "No username"
        mention = user.mention
        bio = user_info.bio or "No bio set"

        msg = await message.reply_text(
            INFO_TEXT.format(id, first_name, last_name, username, mention, status, dc_id, bio),
            parse_mode="HTML"
        )

        await asyncio.sleep(20)
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"<b>Error:</b> <code>{str(e)}</code>", parse_mode="HTML")
