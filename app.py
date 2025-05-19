import os, asyncio
import pytz
from os.path import join, dirname
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Replace these with your own values from https://my.telegram.org
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHAT_ID = os.getenv('CHAT_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Define where the session will be stored (in the Azure File Share)
session_file_path = '/app/session_data/string_session.txt'

def load_string_session():
    """Load the StringSession from the file if it exists."""
    if os.path.exists(session_file_path):
        with open(session_file_path, 'r') as f:
            session_string = f.read().strip()
            print(f"Loaded session: {session_string[:10]}...")  # Log partial session
            return StringSession(session_string)
    else:
        print("No existing session file found, using a new session.")
        return StringSession()  # Create a new session if no file exists

async def save_string_session(client):
    """Save the StringSession to the file."""
    session_string = client.session.save()
    with open(session_file_path, 'w') as f:
        f.write(session_string)
    print(f"Session saved: {session_string[:10]}...")  # Log partial session

def schedule_save(client, loop):
    """Schedule the periodic session save every 10 minutes."""
    scheduler = AsyncIOScheduler(event_loop=loop)
    
    def save_session_job():
        asyncio.run_coroutine_threadsafe(save_string_session(client), loop)
    
    scheduler.add_job(save_session_job, 'interval', minutes=10)
    scheduler.start()

async def main():
    # Load the session from file or create a new one
    session = load_string_session()

    # Start the Telegram client
    async with TelegramClient(session, api_id=int(API_ID), api_hash=str(API_HASH)) as client:
        print("Logged in to Telegram")

        # Schedule session saving
        loop = asyncio.get_running_loop()
        schedule_save(client, loop)

        @client.on(events.Album(chats=int(CHAT_ID)))
        async def albumhandler(event):
            # Forwarding the album as a whole to some chat
            await event.forward_to(int(CHANNEL_ID))
            print(f"Album from {event.sender_id}: {event.text}")

        # Add the event handler for new messages
        @client.on(events.NewMessage(chats=int(CHAT_ID)))
        async def newmessagehandler(event):
            # await handle_new_message(event)
            if not event.message.grouped_id:
                await event.forward_to(int(CHANNEL_ID))
                print(f"Message from {event.sender_id}: {event.text}")

        @client.on(events.MessageEdited(chats=int(CHAT_ID)))
        async def editedmessagehandler(event):
            # Convert the UTC date to Jerusalem timezone
            jerusalem_timezone = pytz.timezone('Asia/Jerusalem')
            event_date_jerusalem = event.date.replace(tzinfo=pytz.UTC).astimezone(jerusalem_timezone)
            formatted_date = event_date_jerusalem.strftime("%Y-%m-%d %H:%M:%S %Z")
            
            # Forwarding the edited message to some chat
            await client.send_message(int(CHANNEL_ID), f"Previous message sent at {formatted_date} was edited to:")
            await event.forward_to(int(CHANNEL_ID))

        # Keep the client running to handle events or updates
        await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())