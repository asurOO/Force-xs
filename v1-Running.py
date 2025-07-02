
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
import asyncio
import time
api_id = 21499823
api_hash = '68b84a62e552690912389c1f746bddfe'
source_channel_id = -2384413951  # CONTENT channel
target_channel_id = 2608691700   # Forward target
client = TelegramClient('forward_session', api_id, api_hash)
forward_count = 0
async def forward_old_messages():
    global forward_count
    source = PeerChannel(source_channel_id)
    target = PeerChannel(target_channel_id)
    async for message in client.iter_messages(source, reverse=True):
        try:
            start = time.time()
            await message.forward_to(target)
            forward_count += 1
            elapsed = (time.time() - start) * 1000
            print(f"[{forward_count}] Forwarded old message in {elapsed:.2f} ms>
        except Exception as e:
            print(f"Failed to forward old message: {e}")
@client.on(events.NewMessage(chats=PeerChannel(source_channel_id)))
async def handler(event):
    global forward_count
    start = time.time()
    try:
        await event.message.forward_to(PeerChannel(target_channel_id))
                          
