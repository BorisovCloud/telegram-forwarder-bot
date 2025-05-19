# telegram-forwarder-bot

This bot forwards messages (including edited messages and albums) from a specified Telegram chat to another Telegram channel, preserving copies of messages that might be edited or deleted by the original sender.

## Features

- Captures new messages and edited messages from a target chat (`CHAT_ID`).
- Forwards these messages (and albums) to a specified channel (`CHANNEL_ID`).
- Stores and updates the Telethon session data in a mounted Azure File Share or local directory.

## Prerequisites

- Python 3.13 or later
- A valid Telegram API ID and API Hash from [my.telegram.org](https://my.telegram.org/)

## Installation and Usage

1. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/telegram-forwarder-bot.git
   cd telegram-forwarder-bot
2. **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Set up your environment variables:**
    
    Copy the format from [`example.env`](./example.env). Update API_ID, API_HASH, CHAT_ID, and CHANNEL_ID.
    ```
    API_ID="123456"
    API_HASH="abc123"
    CHAT_ID="123456789"
    CHANNEL_ID="-100123456789"
    ...
5. **Run the bot:**
    ```bash
    python app.py
    ```
    The bot will log in to Telegram and begin listening for new or edited messages in your target chat.

## Docker Usage
A basic [`Dockerfile`](./Dockerfile) is provided:
1. **Build the image:**
    ```bash
    docker build -t telegram-forwarder-bot .
2. **Run the container (make sure to specify required environment variables):**
    ```bash
    docker run \
        -e API_ID="123456" \
        -e API_HASH="abc123" \
        -e CHAT_ID="123456789" \
        -e CHANNEL_ID="-100123456789" \
        telegram-forwarder-bot

## License
This project is licensed under the [MIT License](./LICENSE). 