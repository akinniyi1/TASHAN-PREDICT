import os
import threading
from datetime import datetime, timedelta
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Bot Configuration ===
BOT_TOKEN        = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG        = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL      = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
PREDICTION_CHANL = "https://t.me/+RNUQHXvEy5w0ZDk1"
REGISTER_LINK    = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"

# === Per-user cooldown tracking ===
user_last_prediction: dict[int, datetime] = {}

# === FastAPI app to bind a port ===
web = FastAPI()
@web.get("/")
def status():
    return {"status": "Tashan Win Prediction Bot is alive"}

# === Telegram Handlers ===

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="predict")],
        [InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK)],
        [InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHANL)],
    ]
    await update.message.reply_text(
        f"🌟 Welcome, {user.first_name}! 🌟\n"
        f"👤 Username: @{(user.username or 'N/A')}\n"
        f"🆔 User ID: {user.id}\n\n"
        "Please select an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def predict(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    now = datetime.utcnow()
    last = user_last_prediction.get(uid)
    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).total_seconds())
        return await query.edit_message_text(f"⏱ Please wait {wait}s before requesting again.")

    user_last_prediction[uid] = now

    # Alternate Big/Small on even/odd minute
    is_even = now.minute % 2 == 0
    purchase = "Big" if is_even else "Small"
    colour   = "Green" if is_even else "Red"
    number   = "0" if is_even else "2"
    image    = IMAGE_BIG if is_even else IMAGE_SMALL

    caption = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {now.strftime('%Y%m%d%H%M')}\n"
        f"💸 Purchase: {purchase}\n\n"
        "🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {colour}\n"
        f"👉🏻 Numbers: {number}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    # Replace the message with a new photo + caption
    await query.edit_message_media(
        media={"type": "photo", "media": image, "caption": caption}
    )

# === Entry Point ===

def main():
    # 1) Start FastAPI on port from env (or 10000)
    def run_api():
        port = int(os.environ.get("PORT", 10000))
        uvicorn.run(web, host="0.0.0.0", port=port)

    threading.Thread(target=run_api, daemon=True).start()

    # 2) Build and run the Telegram bot (sync)
    app_bot = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(predict, pattern="predict"))

    # This will initialize, start polling, and block forever
    app_bot.run_polling()

if __name__ == "__main__":
    main()
