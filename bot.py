python
import os
import asyncio
from rubpy import Client, handlers
from rubpy.types import Updates
import yt_dlp
import tempfile

bot = Client(name="rubika_music_bot")

@bot.on(handlers.MessageUpdates(["Text"]))
async def message_handler(update: Updates):
    message = update.message
    text = message.text
    
    if text.startswith("/start"):
        await message.reply("🎵 سلام! لینک آهنگ یا ویدیو از یوتیوب، اینستاگرام و... رو بفرست تا برات دانلود کنم.")
        return
    
    if text.startswith(("http://", "https://")):
        await message.reply("⏳ در حال دریافت... لطفاً صبر کن")
        
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tempfile.gettempdir(), '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file_path = ydl.prepare_filename(info)
                
                audio_file = file_path.rsplit('.', 1)[0] + '.mp3'
                
                if os.path.exists(file_path):
                    os.rename(file_path, audio_file)
                    await message.reply_file(audio_file)
                    os.remove(audio_file)
                else:
                    await message.reply("❌ خطا در دانلود فایل")
                    
        except Exception as e:
            await message.reply(f"❌ خطا: {str(e)[:100]}")
    else:
        await message.reply("❌ لطفاً یک لینک معتبر بفرست")

bot.run()
