import os, threading, asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ── CONFIG ─────────────────────────────────────────────────────────────
BOT_TOKEN        = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG        = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL      = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
REGISTER_LINK    = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHNL  = "https://t.me/+RNUQHXvEy5w0ZDk1"

# ── STATE ───────────────────────────────────────────────────────────────
user_last: dict[int, datetime] = {}

# ── FASTAPI ────────────────────────────────────────────────────────────
web = FastAPI()

@web.get("/")
def health():
    return {"status": "Tashan Win Bot alive"}

# ── TELEGRAM HANDLERS ──────────────────────────────────────────────────

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get")],
        [InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK)],
        [InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHNL)],
    ]
    await update.message.reply_text(
        f"🌟 Welcome, {user.first_name}! 🌟\n"
        f"🆔 {user.id}",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def get(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()

    now = datetime.utcnow()
    last = user_last.get(uid)
    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).seconds)
        return await q.edit_message_text(f"⏱ Wait {wait}s for new prediction.")

    user_last[uid] = now
    even = now.minute % 2 == 0
    purchase = "Big" if even else "Small"
    colour   = "Green" if even else "Red"
    number   = "0" if even else "2"
    image    = IMAGE_BIG if purchase=="Big" else IMAGE_SMALL

    text = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {now.strftime('%Y%m%d%H%M')}\n"
        f"💸 Purchase: {purchase}\n\n"
        f"🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {colour}\n"
        f"👉🏻 Numbers: {number}\n\n"
        "💡 Strategy Tip:\nUse the 2x strategy for better chances.\n\n"
        "📊 Fund Management:\nAlways play through fund management 5 level."
    )

    await q.edit_message_media(
        media={"type":"photo","media":image,"caption":text}
    )

# ── RUNNER ─────────────────────────────────────────────────────────────

def main():
    # 1) start FastAPI
    def run_web():
        uvicorn.run(web, host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
    threading.Thread(target=run_web, daemon=True).start()

    # 2) start Telegram bot
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(get, pattern="get"))
    bot.run_polling()

if __name__ == "__main__":
    main()
