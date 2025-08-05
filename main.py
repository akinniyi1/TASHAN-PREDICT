from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import asyncio
from datetime import datetime

# 🔐 Your bot token
BOT_TOKEN = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"

# 🖼 Hosted images
BIG_IMAGE = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
SMALL_IMAGE = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"

# 📢 Register link and channel
REGISTER_LINK = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHANNEL = "https://t.me/+RNUQHXvEy5w0ZDk1"

# Set up logging
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="predict")],
        [InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK)],
        [InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHANNEL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\nYour Telegram ID: `{user.id}`",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Alternate between BIG and SMALL every minute
    current_minute = datetime.utcnow().minute
    if current_minute % 2 == 0:
        text = "📢 Prediction: SELECT BIG"
        image_url = BIG_IMAGE
    else:
        text = "📢 Prediction: SELECT SMALL"
        image_url = SMALL_IMAGE

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, caption=text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_prediction, pattern="predict"))
    app.run_polling()
