import os
import asyncio
from fastapi import FastAPI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from datetime import datetime, timedelta

# === Bot Configuration ===
BOT_TOKEN = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
PREDICTION_CHANNEL = "https://t.me/+RNUQHXvEy5w0ZDk1"
REGISTER_LINK = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"

# === User state for last prediction time ===
user_last_prediction = {}

# === Web App ===
app = FastAPI()

@app.get("/")
def home():
    return {"status": "Tashan Win Prediction Bot running"}

# === Telegram Bot Handlers ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get_prediction")],
        [InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK)],
        [InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHANNEL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Welcome {user.first_name}!\n\nYour ID: {user.id}\n\n"
        "Use the buttons below to get started with Tashan Win 🔥",
        reply_markup=reply_markup
    )

async def get_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    now = datetime.utcnow()
    last_time = user_last_prediction.get(user_id)
    
    # If user has used it and it's less than 60 seconds
    if last_time and (now - last_time).total_seconds() < 60:
        await query.edit_message_text("⏱ Please wait 60 seconds before requesting another prediction.")
        return

    user_last_prediction[user_id] = now

    # Alternate prediction logic based on even/odd minutes
    minute = now.minute
    is_even = minute % 2 == 0
    purchase = "Big" if is_even else "Small"
    color = "Green" if is_even else "Red"
    number = "0" if is_even else "2"
    image_url = IMAGE_BIG if purchase == "Big" else IMAGE_SMALL

    prediction_text = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {now.strftime('%Y-%m-%d %H:%M')}\n"
        f"💸 Purchase: {purchase}\n\n"
        f"🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {color}\n"
        f"👉🏻 Numbers: {number}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    await query.edit_message_media(
        media={
            "type": "photo",
            "media": image_url,
            "caption": prediction_text
        }
    )

# === Main function to run both bot and web ===

async def main():
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CallbackQueryHandler(get_prediction))

    # Start bot polling in background
    await telegram_app.initialize()
    await telegram_app.start()
    print("Telegram bot started...")

    # Keep the bot running
    await telegram_app.updater.start_polling()
    await telegram_app.updater.idle()

# Run both FastAPI and bot
if __name__ == "__main__":
    import uvicorn
    import threading

    # Run FastAPI in a thread
    def run_web():
        uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

    threading.Thread(target=run_web).start()

    # Run the bot in asyncio event loop
    asyncio.run(main())
