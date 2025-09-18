import os
import threading
from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from PIL import Image, ImageEnhance

# 🔑 Config (Direct set किया है)
API_ID = 21302239
API_HASH = "1560930c983fbca6a1fcc8eab760d40d"
BOT_TOKEN = "8032481645:AAEQuyNikhxdSIc9tXk8QTotj-JmvJUpcdg"

app = Client(
    "ImageEnhancerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
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
        "👋 Welcome to **HD Image Enhancer Bot**!\n\n"
        "📷 कोई भी photo भेजो → मैं उसे HD quality में enhance कर दूँगा ✨\n\n"
        "⚡ Natural look रहेगा, over-process नहीं होगा!"
    )

# 📷 Handle photo
@app.on_message(filters.photo & filters.private)
async def enhance_photo(client: Client, message: Message):
    try:
        status = await message.reply_text("🔄 Processing your photo...")

        # Download image
        file_path = await client.download_media(message.photo.file_id, file_name="input.jpg")

        # Open image with Pillow
        img = Image.open(file_path)

        # Apply natural enhancements
        img = ImageEnhance.Brightness(img).enhance(1.1)  # हल्का bright
        img = ImageEnhance.Contrast(img).enhance(1.15)   # contrast improve
        img = ImageEnhance.Sharpness(img).enhance(1.2)   # sharp
        img = ImageEnhance.Color(img).enhance(1.1)       # natural colors

        # Save output
        output_path = "enhanced.jpg"
        img.save(output_path, "JPEG")

        # Send enhanced photo
        await message.reply_photo(output_path, caption="✨ Here is your enhanced HD photo!")

        # Cleanup
        os.remove(file_path)
        os.remove(output_path)
        await status.delete()

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("🚀 HD Image Enhancer Bot started...")
    app.run()
