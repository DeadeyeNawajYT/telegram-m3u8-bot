import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_m3u8(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    output = "video.mp4"

    await update.message.reply_text("Downloading and converting your video...")

    try:
        subprocess.run([
            "ffmpeg", "-i", url,
            "-c", "copy", "-bsf:a", "aac_adtstoasc", output
        ], check=True)

        await update.message.reply_video(
            video=open(output, "rb"),
            supports_streaming=True,
            caption="Here is your video!"
        )

        os.remove(output)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if name == "main":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_m3u8))
    app.run_polling()
