import os
import threading
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask

# 🔑 Config (Environment Variables से)
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

app = Client(
    "ImageEnhancerBot",
    api_id=21302239,
    api_hash=1560930c983fbca6a1fcc8eab760d40d,
    bot_token=8032481645:AAEQuyNikhxdSIc9tXk8QTotj-JmvJUpcdg
)

# Dummy Flask app for Render (port binding)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Image Enhancer Bot is running on Render!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)

# 🎬 Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message: Message):
    await message.reply_text(
        "👋 Welcome to **Image Enhancer Bot**!\n\n"
        "📷 Just send me a photo and I’ll enhance it using AI ✨\n\n"
        "Powered by **Real-ESRGAN** 🚀"
    )

# 📷 Handle photo
@app.on_message(filters.photo & filters.private)
async def enhance_photo(client: Client, message: Message):
    try:
        status = await message.reply_text("🔄 Processing your photo, please wait...")

        # Download image
        file_path = await client.download_media(message.photo.file_id, file_name="input.jpg")

        # Output path
        output_path = "enhanced.jpg"

        # Run Real-ESRGAN enhancement (must be installed in requirements.txt)
        subprocess.run(
            ["realesrgan-ncnn-vulkan", "-i", file_path, "-o", output_path],
            check=True
        )

        # Send enhanced image
        await message.reply_photo(output_path, caption="✨ Here is your enhanced photo!")

        # Cleanup
        os.remove(file_path)
        os.remove(output_path)
        await status.delete()

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🚀 Image Enhancer Bot started...")
    app.run()
