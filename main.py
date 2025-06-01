from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters
from telegram.ext import Application

# توکن ربات و چت آیدی مقصد رو مستقیم اینجا می‌نویسیم (فقط برای استفاده شخصی!)
TOKEN = "8147264789:AAF6c-Ru9WNP2SCJFigJYY2PR1CalDKZQco"
DEST_CHAT_ID = "5901291262"  # آیدی کاربر مقصد

app = Flask(__name__)
bot = Bot(token=TOKEN)

application = Application.builder().token(TOKEN).build()
dispatcher = Dispatcher(bot=bot, update_queue=None, application=application)

def relay_message(update: Update, context):
    message = update.effective_message

    if message.text:
        bot.send_message(chat_id=DEST_CHAT_ID, text=message.text)
    elif message.photo:
        bot.send_photo(chat_id=DEST_CHAT_ID, photo=message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        bot.send_video(chat_id=DEST_CHAT_ID, video=message.video.file_id, caption=message.caption)
    elif message.document:
        bot.send_document(chat_id=DEST_CHAT_ID, document=message.document.file_id, caption=message.caption)
    else:
        bot.send_message(chat_id=DEST_CHAT_ID, text="نوع پیام پشتیبانی نمی‌شود.")

dispatcher.add_handler(MessageHandler(filters.ALL, relay_message))

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "ربات فعال است"
