from telethon.utils import resolve_invite_link
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from Sibyl_System.plugins.Mongo_DB.tree import add_developer, add_manager, get_data
from Sibyl_System import MANAGERS, DEVELOPERS, CARDINAL, session
from Sibyl_System import System, system_cmd
from Sibyl_System import Sibyl_logs

from datetime import datetime
from urllib.parse import urlparse, urlunparse
import heroku3
import os
import re
import json

try:
    from Sibyl_System import HEROKU_API_KEY, HEROKU_APP_NAME

    heroku_conn = heroku3.from_key(HEROKU_API_KEY)
    app = heroku_conn.app(HEROKU_APP_NAME)
    config = app.config()
    HEROKU = True
except BaseException:
    HEROKU = False

json_file = os.path.join(os.getcwd(), "Sibyl_System\\elevated_users.json")


@System.on(system_cmd(pattern=r"addsbm", allow_developers=True))
async def addsbm(event) -> None:
    if event.message.reply_to_msg_id:
        replied = await event.get_reply_message()
        if replied:
            u_id = replied.sender.id
        else:
            return
    else:
        u_id = event.text.split(" ", 2)[1]
        try:
            u_id = (await System.get_entity(u_id)).id
        except BaseException:
            await event.reply(
                "I haven't interacted with that user! Meh, Will add them anyway"
            )
    if u_id in MANAGERS:
        await System.send_message(event.chat_id, "That person is already Manager!")
        return
    if HEROKU:
        config["MANAGERS"] = os.environ.get("MANAGERS") + " " + str(u_id)
    else:
        with open(json_file, "r") as file:
            data = json.load(file)
        data["MANAGERS"].append(u_id)
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        await System.send_message(event.chat_id, "Added to spam block managers, Restarting...")
        if not event.from_id.user_id in CARDINAL:
            await add_manager(event.from_id.user_id, u_id)
        await System.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()
    if not event.from_id.user_id in CARDINAL:
        await add_enforcers(event.from_id.user_id, u_id)
    await System.send_message(
        event.chat_id, f"Added [{u_id}](tg://user?id={u_id}) to Spam block Managers, Restarting..."
    )


@System.on(system_cmd(pattern=r"rsbm", allow_developers=True))
async def rsbm(event) -> None:
    if event.message.reply_to_msg_id:
        replied = await event.get_reply_message()
        u_id = replied.sender.id
    else:
        u_id = event.text.split(" ", 2)[1]
    try:
        u_id = (await System.get_entity(u_id)).id
    except BaseException:
        await event.reply("Invalid ID/Username!")
    u_id = int(u_id)
    if u_id not in MANAGERS:
        await System.send_message(event.chat_id, "Is that person even a Manager?")
        return
    if HEROKU:
        str(u_id)
        ENF = os.environ.get("MANAGERS")
        if ENF.endswith(u_id):
            config["MANAGERS"] = ENF.strip(" " + str(u_id))
        elif ENF.startswith(u_id):
            config["MANAGERS"] = ENF.strip(str(u_id) + " ")
        else:
            config["MANAGERS"] = ENF.strip(" " + str(u_id) + " ")
    else:
        with open(json_file, "r") as file:
            data = json.load(file)
        data["MANAGERS"].remove(u_id)
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        await System.send_message(
            event.chat_id, "Removed from Spam block managers, Restarting..."
        )
        await System.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()
    await System.send_message(
        event.chat_id, f"Removed [{u_id}](tg://user?id={u_id}) from Managers"
    )


@System.on(system_cmd(pattern=r"managers", allow_developers=True))
async def listuser(event) -> None:
    msg = "Managers:\n"
    for z in MANAGERS:
        try:
            user = await System.get_entity(z)
            msg += f"•[{user.first_name}](tg://user?id={user.id}) | {z}\n"
        except BaseException:
            msg += f"•{z}\n"
    await System.send_message(event.chat_id, msg)


@System.on(system_cmd(pattern=r"join", allow_developers=True))
async def join(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    private = re.match(
        r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)", link
    )
    if private:
        await System(ImportChatInviteRequest(private.group(5)))
        await System.send_message(event.chat_id, "Joined chat!")
        await System.send_message(
            Sibyl_logs,
            f"{(await event.get_sender()).first_name} made Spam Blocker join {private.group(5)}",
        )
    else:
        await System(JoinChannelRequest(link))
        await System.send_message(event.chat_id, "Joined chat!")
        await System.send_message(
            Sibyl_logs,
            f"{(await event.get_sender()).first_name} made Spam Blocker join {link}",
        )


@System.on(system_cmd(pattern=r"adddev"))
async def adddev(event) -> None:
    if event.reply:
        replied = await event.get_reply_message()
        if replied:
            u_id = replied.sender.id
        else:
            return
    else:
        u_id = event.text.split(" ", 2)[1]
    try:
        u_id = (await System.get_entity(u_id)).id
    except BaseException:
        await event.reply("Ivalid ID/Username!")
        return
    if u_id in DEVELOPERS:
        await System.send_message(event.chat_id, "That person is already an Developer!")
        return
    if HEROKU:
        config["DEVELOPERS"] = os.environ.get("DEVELOPERS") + " " + str(u_id)
    else:
        with open(json_file, "r") as file:
            data = json.load(file)
        data["DEVELOPERS"].append(u_id)
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        await System.send_message(event.chat_id, "Added to Developers, Restarting...")
        await add_developer(event.from_id.user_id, u_id)
        await System.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()
    await add_developer(event.from_id.user_id, u_id)
    await System.send_message(
        event.chat_id, f"Added [{u_id}](tg://user?id={u_id}) to DEVELOPERS, Restarting..."
    )


@System.on(system_cmd(pattern=r"rmdev"))
async def rmdev(event) -> None:
    if event.message.reply_to_msg_id:
        replied = await event.get_reply_message()
        u_id = replied.sender.id
    else:
        u_id = event.text.split(" ", 2)[1]
    try:
        u_id = (await System.get_entity(u_id)).id
    except BaseException:
        await event.reply("Ivalid ID/Username!")
    if u_id not in DEVELOPERS:
        await System.send_message(event.chat_id, "Is that person even an Developer?")
        return
    u_id = str(u_id)
    if HEROKU:
        ENF = os.environ.get("DEVELOPERS")
        if ENF.endswith(u_id):
            config["DEVELOPERS"] = ENF.strip(" " + str(u_id))
        elif ENF.startswith(u_id):
            config["DEVELOPERS"] = ENF.strip(str(u_id) + " ")
        else:
            config["DEVELOPERS"] = ENF.strip(" " + str(u_id) + " ")
    else:
        with open(json_file, "r") as file:
            data = json.load(file)
        data["DEVELOPERS"].remove(u_id)
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
        await System.send_message(
            event.chat_id, "Removed from Developers, Restarting..."
        )
        await System.disconnect()
        os.execl(sys.executable, sys.executable, *sys.argv)
        quit()
    await System.send_message(
        event.chat_id,
        f"Removed Developer status of [{u_id}](tg://user?id={u_id}), Now that user is a mere manager.",
    )


@System.on(system_cmd(pattern=r"info ", allow_developers=True))
async def info(event) -> None:
    data = (await get_data())["standalone"]
    if not event.text.split(" ", 1)[1] in data.keys():
        return
    u = event.text.split(" ", 1)[1]
    msg = f"User: {u}\n"
    msg += f"Added by: {data[u]['addedby']}\n"
    msg += f"Timestamp: {datetime.fromtimestamp(data[u]['timestamp']).strftime('%d/%m/%Y - %H:%M:%S')}(`{data[u]['timestamp']}`)"
    await event.reply(msg)


@System.on(system_cmd(pattern=r"developers", allow_developers=True))
async def listuserI(event) -> None:
    msg = "Developers:\n"
    for z in DEVELOPERS:
        try:
            user = await System.get_entity(z)
            msg += f"•[{user.first_name}](tg://user?id={user.id}) | {z}\n"
        except BaseException:
            msg += f"•{z}\n"
    await System.send_message(event.chat_id, msg)


@System.on(system_cmd(pattern=r"resolve", allow_developers=True))
async def resolve(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    match = re.match(
        r"(https?://)?(www\.)?t(elegram)?\.(dog|me|org)/joinchat/(.*)", link
    )
    if match:
        try:
            data = resolve_invite_link(match.group(5))
        except BaseException:
            await System.send_message(
                event.chat_id, "Couldn't fetch data from that link"
            )
            return
        await System.send_message(
            event.chat_id,
            f"Info from hash {match.group(5)}:\n**Link Creator**: {data[0]}\n**Chat ID**: {data[1]}",
        )


@System.on(system_cmd(pattern=r"leave"))
async def leave(event) -> None:
    try:
        link = event.text.split(" ", 1)[1]
    except BaseException:
        return
    c_id = re.match(r"-(\d+)", link)
    if c_id:
        await System(LeaveChannelRequest(int(c_id.group(0))))
        await System.send_message(
            event.chat_id, f"Cardinal has left chat with id[-{c_id.group(1)}]"
        )
    else:
        await System(LeaveChannelRequest(link))
        await System.send_message(event.chat_id, f"Cardinal has left chat[{link}]")


@System.on(system_cmd(pattern=r"get_redirect ", allow_developers=True))
async def redirect(event) -> None:
    try:
        of = event.text.split(" ", 1)[1]
    except BaseException:
        return
    of = urlunparse(urlparse(of, "https"))
    async with session.get(of) as r:
        url = r.url
    await System.send_message(event.chat_id, f"URL: {url}")


help_plus = """
Help!
`join` - Joins a chat.
Format : join <chat username or invite link>
`leave` - Leaves a chat.
Format : leave <chat username or id>
`resolve` - Resolve a chat invite link.
Format : resolve <chat invite link>
`get_redirect` - Follows redirect of a link.
Format : get_redirect <URL>
**Notes:**
`/` `?` `.` `!` are supported prefixes.
**Example:** `/join` or `?join` or `.join`
"""

__plugin_name__ = "extras"
