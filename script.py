from telethon.sync import TelegramClient, events
from telethon.tl.types import UpdateChatDefaultBannedRights
import traceback
import time
import os
from os import environ

api_id = environ['api_id']
api_hash = environ['api_hash']
#Enter your phone number.
session_name = environ['session_name']
group_username = environ['group_username']
send_msg = environ['send_msg']

print("[+] Script started")
client = TelegramClient(session_name, api_id, api_hash).start(session_name)
if client.is_user_authorized():
    print("[+] Logged in sucessfully")
else:
    print("[-] Error while Logging in, please try again")
    exit()

@client.on(events.Raw(types=UpdateChatDefaultBannedRights))
async def read_new_message(event):
    try:
        group_data = await client.get_entity(group_username)
        #print(event)
        #print(event.peer.chat_id, event.default_banned_rights.send_messages)
        try:
            ids = event.peer.chat_id 
        except:
            pass
        try:
            ids = event.peer.channel_id
        except:
            pass
        if ids == group_data.id  and not event.default_banned_rights.send_messages:
            print("\n[+] Sending Message")
            await client.send_message(group_data, send_msg)
            print("[+] Message Sent")
    except:
        traceback.print_exc()
    raise events.StopPropagation

client.run_until_disconnected()
