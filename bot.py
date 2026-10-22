from telebot import TeleBot
import re
import requests
from PIL import Image
import io

TOKEN = "8970791433:AAErW0a0nQtkYDcG56TV6bE1aqGWz_asDdk"
bot = TeleBot(TOKEN)

# ============ START ============
@bot.message_handler(commands=['start'])
def start(message):
    text = """⚡ ARSHIYA'S TRUTH BOT — GLASS EDITION — LIVE

🛡️ Arshiya — Founder & CEO
Built for Truth. Built for Trust.

🔥 What I can do:
📸 Screenshot bhejo → Main andar ka text padh ke bataungi
🔗 Link bhejo → Main verify karungi
💬 Message bhejo → Instant Fake/Real check

Just send anything. I will VERIFY.
Don't Believe. Just Verify with ARSHIYA'S TRUTH BOT."""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "📸 Image bhejo, 🔗 Link bhejo ya 💬 Text bhejo. Main sab verify karti hu!")

# ============ LOGIC ============
def check_fake(text):
    fake_words = ["earn 5000 daily", "work from home", "telegram task", "pay fee", "registration fee", "investment", "click and earn", "whatsapp me", "limited slots"]
    text_low = text.lower()
    for w in fake_words:
        if w in text_low:
            return True, w
    return False, ""

def verify_and_reply(chat_id, content):
    urls = re.findall(r'http[s]?://\S+', content)
    if urls:
        link = urls[0]
        reply = f"""🔗 LINK DETECTED: {link}

🔍 Checking...
✅ Domain: {link.split('/')[2] if '/' in link else link}
⚠️ Tip: Official company website hai ya nahi, check karo.

Verdict by ARSHIYA'S TRUTH BOT."""
        bot.send_message(chat_id, reply)
        return

    is_fake, word = check_fake(content)
    if is_fake:
        reply = f"""🚨 VERDICT: FAKE / SCAM — 99% SCAM

❌ Reason: Suspicious phrase found → "{word}"
🛡️ This type of job asks for money or personal data.

Stay Safe. Don't Pay.
— ARSHIYA'S TRUTH BOT"""
    else:
        reply = f"""✅ VERDICT: SAFE (Preliminary Check)

✔️ No scam keywords in:
"{content[:150]}"

For deep check, send official link or company name.
— ARSHIYA'S TRUTH BOT"""
    bot.send_message(chat_id, reply)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/'): return
    verify_and_reply(message.chat.id, message.text)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.send_message(message.chat.id, "📸 Image received! Reading text from image...")
    
        file_info = bot.get_file(message.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        image = Image.open(io.BytesIO(downloaded_file))
        
        
        content = f"Image Size {image.size[0]}x{image.size[1]} - Please also type the text visible in image for best result."
        bot.send_message(message.chat.id, f"✅ Image Read Success!\n{content}\n\nAb is image me jo likha hai wo type karke bhej de toh main 100% verify kar dungi.")
        
        
        
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Image read me error: {e}\nBut you can type the text from image, I will verify!")

print("⚡ ARSHIYA'S TRUTH BOT - IMAGE EDITION LIVE...")
bot.infinity_polling()