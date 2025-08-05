import os, threading
from datetime import datetime, timedelta
from fastapi import FastAPI
import uvicorn

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ── CONFIG ───────────────────────────────────────────────────────────────
BOT_TOKEN       = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG       = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL     = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
REGISTER_LINK   = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHNL = "https://t.me/+RNUQHXvEy5w0ZDk1"

# ── STATE ────────────────────────────────────────────────────────────────
user_last: dict[int, datetime] = {}

# ── FASTAPI HEALTHCHECK ─────────────────────────────────────────────────
web = FastAPI()

@web.get("/")
def health():
    return {"status": "Tashan Win Bot alive"}

# ── KEYBOARDS ────────────────────────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 Get Prediction",   callback_data="get")],
        [
            InlineKeyboardButton("🔗 Register Link",      url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHNL)
        ]
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")]
    ])

# ── HANDLERS ─────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handles both /start and back_to_menu callbacks."""
    # If callback_query, edit that message; if message, send new
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=f"🌟 Welcome, {update.effective_user.first_name}! 🌟\n🆔 {update.effective_user.id}",
            reply_markup=main_menu_keyboard()
        )
    else:
        await update.message.reply_text(
            f"🌟 Welcome, {update.effective_user.first_name}! 🌟\n🆔 {update.effective_user.id}",
            reply_markup=main_menu_keyboard()
        )

async def get_prediction(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid  = query.from_user.id
    now  = datetime.utcnow()
    last = user_last.get(uid)
    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).seconds)
        return await query.edit_message_text(f"⏱ Please wait {wait}s before your next prediction.", reply_markup=back_keyboard())

    user_last[uid] = now

    purchase = "Big" if now.minute % 2 == 0 else "Small"
    n1, n2   = __import__("random").sample(range(1, 10), 2)
    period   = now.strftime("%Y%m%d%H%M")
    colour   = __import__("random").choice(["Green", "Violet"])
    image    = IMAGE_BIG if purchase == "Big" else IMAGE_SMALL

    caption = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {period}\n"
        f"💸 Purchase: {purchase}\n\n"
        "🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {colour}\n"
        f"👉🏻 Numbers: {n1} or {n2}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    await query.edit_message_media(
        media={"type":"photo","media":image,"caption":caption},
        reply_markup=back_keyboard()
    )

# ── ENTRY POINT ──────────────────────────────────────────────────────────
def main():
    # 1) Start FastAPI in background
    def run_api():
        uvicorn.run(web, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    threading.Thread(target=run_api, daemon=True).start()

    # 2) Build and run Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start,          pattern="back_to_menu"))
    app.add_handler(CallbackQueryHandler(get_prediction, pattern="get"))

    # Drop any pending updates on startup to avoid conflicts
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
