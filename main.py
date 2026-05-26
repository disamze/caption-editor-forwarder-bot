from pyrogram import Client, filters
from pyrogram.types import Message
import os

# =========================
# TELEGRAM API DETAILS
# =========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# =========================
# BOT CLIENT
# =========================

app = Client(
    "caption-editor-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# =========================
# SOURCE CHANNEL ID
# (Where bot reads posts from)
# =========================

SOURCE_CHANNEL = -1003949636049

# =========================
# TARGET GROUP ID
# (Where bot sends edited posts)
# =========================

TARGET_GROUP = -1003732913181

# =========================
# TOPIC ID
# (Topic/thread inside group)
# =========================

TOPIC_ID = 9599

# =========================
# WORDS TO REMOVE
# =========================

REMOVE_WORDS = [
    "Extracted By: GHOST",
    
]

# =========================
# DEFAULT TEXT TO ADD
# =========================

DEFAULT_TEXT = """

━━━━━━━━━━━━━━━
✨ Powered By @Allcompetetiveexamsbooks

🔥 Join https://t.me/Allcompetetiveexamsbooks For More lectures
━━━━━━━━━━━━━━━
"""

# =========================
# CAPTION EDIT FUNCTION
# =========================

def edit_caption(caption):

    if not caption:
        return DEFAULT_TEXT.strip()

    new_caption = caption

    # REMOVE UNWANTED WORDS
    for word in REMOVE_WORDS:
        new_caption = new_caption.replace(word, "")

    # REMOVE EXTRA SPACES
    new_caption = "\n".join(
        line.strip() for line in new_caption.splitlines() if line.strip()
    )

    # ADD YOUR TEXT
    new_caption += "\n" + DEFAULT_TEXT

    return new_caption.strip()

# =========================
# MAIN MESSAGE HANDLER
# =========================

@app.on_message(filters.chat(SOURCE_CHANNEL))
async def forward_post(client, message: Message):

    caption = message.caption or message.text or ""

    edited_caption = edit_caption(caption)

    try:

        # =========================
        # PHOTO
        # =========================
        if message.photo:

            await client.send_photo(
                chat_id=TARGET_GROUP,
                photo=message.photo.file_id,
                caption=edited_caption,
                message_thread_id=TOPIC_ID
            )

        # =========================
        # VIDEO
        # =========================
        elif message.video:

            await client.send_video(
                chat_id=TARGET_GROUP,
                video=message.video.file_id,
                caption=edited_caption,
                message_thread_id=TOPIC_ID
            )

        # =========================
        # DOCUMENT
        # =========================
        elif message.document:

            await client.send_document(
                chat_id=TARGET_GROUP,
                document=message.document.file_id,
                caption=edited_caption,
                message_thread_id=TOPIC_ID
            )

        # =========================
        # AUDIO
        # =========================
        elif message.audio:

            await client.send_audio(
                chat_id=TARGET_GROUP,
                audio=message.audio.file_id,
                caption=edited_caption,
                message_thread_id=TOPIC_ID
            )

        # =========================
        # TEXT MESSAGE
        # =========================
        elif message.text:

            await client.send_message(
                chat_id=TARGET_GROUP,
                text=edited_caption,
                message_thread_id=TOPIC_ID
            )

        print("Message forwarded successfully")

    except Exception as e:
        print("ERROR:", e)

# =========================
# START BOT
# =========================

print("Bot Started Successfully...")
app.run()