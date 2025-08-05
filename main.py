import os, threading
from datetime import datetime, timedelta
from fastapi import FastAPI
import uvicorn

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ── CONFIG ─────────────────────────────────────────────────────────────
BOT_TOKEN       = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG       = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL     = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
REGISTER_LINK   = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHNL = "https://t.me/+RNUQHXvEy5w0ZDk1"

# ── STATE ───────────────────────────────────────────────────────────────
user_last: dict[int, datetime] = {}

# ── FASTAPI HEALTHCHECK ──────────────────────────────────────────────────
web = FastAPI()

@web.get("/")
def health():
    return {"status": "Tashan Win Bot alive"}

# ── BUILD MAIN MENU KEYBOARD ─────────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get")],
        [
            InlineKeyboardButton("🔗 Register Link",      url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHNL)
        ]
    ])

# ── /start HANDLER ──────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Show the main menu."""
    if update.message:
        target = update.message
        send = target.reply_text
    else:
        # callback_query → re-edit
        target = update.callback_query.message
        send = target.edit_text

    user = update.effective_user
    text = (
        f"🌟 Welcome, {user.first_name}! 🌟\n"
        f"🆔 {user.id}"
    )
    await send(text, reply_markup=main_menu_keyboard())

# ── get_prediction HANDLER ──────────────────────────────────────────────
async def get_prediction(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Generate & send a new prediction (or tell to wait)."""
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    now = datetime.utcnow()
    last = user_last.get(uid)

    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).seconds)
        return await query.edit_message_text(f"⏱ Please wait {wait}s before your next prediction.")

    user_last[uid] = now

    # Even/odd minute for Big/Small
    purchase = "Big" if now.minute % 2 == 0 else "Small"
    # Two random numbers 1–9
    n1, n2 = __import__("random").sample(range(1, 10), 2)
    period = now.strftime("%Y%m%d%H%M")

    caption = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {period}\n"
        f"💸 Purchase: {purchase}\n\n"
        "🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {__import__('random').choice(['Green','Violet'])}\n"
        f"👉🏻 Numbers: {n1} or {n2}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    # back button under prediction
    back_kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 Back to Menu", callback_data="start")
    ]])

    # edit message to photo+caption+back button
    await query.edit_message_media(
        media={"type":"photo","media": IMAGE_BIG if purchase=="Big" else IMAGE_SMALL, "caption": caption},
        reply_markup=back_kb
    )

# ── RUNNER ───────────────────────────────────────────────────────────────
def main():
    # 1) Start FastAPI healthcheck
    def run_web():
        uvicorn.run(web, host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
    threading.Thread(target=run_web, daemon=True).start()

    # 2) Start Telegram bot
    bot = ApplicationBuilder().token(BOT_TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(get_prediction, pattern="get"))
    bot.add_handler(CallbackQueryHandler(start,           pattern="start"))
    bot.run_polling()

if __name__ == "__main__":
    main()
