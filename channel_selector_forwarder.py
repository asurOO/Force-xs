import json
import asyncio
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.messages import ForwardMessagesRequest, GetHistoryRequest
from InquirerPy import inquirer

# ========== CONFIG ==========
api_id = 21499823
api_hash = '68b84a62e552690912389c1f746bddfe'
session_name = 'my_session'
channel_list_file = "channels.json"
forward_interval_seconds = 60  # every 60 seconds check for new messages
# ============================

# Load channels
def load_channels():
    with open(channel_list_file, "r", encoding="utf-8") as f:
        return json.load(f)

# Select using arrow keys
def select_channel(prompt_text, channels):
    choices = [f"{ch['title']} (ID: {ch['id']})" for ch in channels]
    selected = inquirer.select(message=prompt_text, choices=choices).execute()
    index = choices.index(selected)
    return channels[index]

# Async main logic
async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    channels = load_channels()

    source = select_channel("📥 Select Source Channel:", channels)
    target = select_channel("📤 Select Target Channel:", channels)

    source_input = InputPeerChannel(source["id"], source["access_hash"])
    target_input = InputPeerChannel(target["id"], target["access_hash"])

    last_forwarded_id = 0

    print(f"\n🔄 Starting auto-forwarding every {forward_interval_seconds} seconds...\n")

    while True:
        try:
            history = await client(GetHistoryRequest(
                peer=source_input,
                limit=10,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=last_forwarded_id,
                add_offset=0,
                hash=0
            ))

            messages = [msg for msg in history.messages if msg.id > last_forwarded_id]
            messages.sort(key=lambda m: m.id)

            if messages:
                for msg in messages:
                    await client(ForwardMessagesRequest(
                        from_peer=source_input,
                        id=[msg.id],
                        to_peer=target_input
                    ))
                    print(f"✅ Forwarded message ID: {msg.id}")
                last_forwarded_id = messages[-1].id
            else:
                print("⏳ No new messages...")

        except Exception as e:
            print(f"⚠️ Error during forwarding: {e}")

        await asyncio.sleep(forward_interval_seconds)

asyncio.run(main())
