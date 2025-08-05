import os, threading
import random
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

# ── CONFIG ────────────────────────────────────────────────────────────────
BOT_TOKEN       = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG       = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL     = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
REGISTER_LINK   = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHNL = "https://t.me/+RNUQHXvEy5w0ZDk1"
SUPPORT_USER    = "@Jennifer_Support"

# ── STATE ────────────────────────────────────────────────────────────────
user_last: dict[int, datetime] = {}

# ── FASTAPI HEALTHCHECK ──────────────────────────────────────────────────
web = FastAPI()
@web.get("/")
def health():
    return {"status": "Tashan Win Bot alive"}

# ── KEYBOARDS ────────────────────────────────────────────────────────────
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        # Row 1: Get Prediction
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get")],
        # Row 2: Register Link & Prediction Channel
        [
            InlineKeyboardButton("🔗 Register Link",      url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHNL)
        ],
        # Row 3: Support
        [InlineKeyboardButton("💁 Support", url=f"https://t.me/{SUPPORT_USER.strip('@')}")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
    ])

# ── HANDLERS ─────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Handles /start and Back button."""
    if update.callback_query:
        await update.callback_query.answer()
        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = update.message.chat_id

    user = update.effective_user
    text = f"🌟 Welcome, {user.first_name}! 🌟\n🆔 {user.id}"
    await ctx.bot.send_message(chat_id=chat_id, text=text, reply_markup=main_menu_keyboard())

async def get_prediction(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Generate or cooldown a prediction."""
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    uid     = query.from_user.id
    now     = datetime.utcnow()
    last    = user_last.get(uid)

    # Cooldown check
    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).seconds)
        return await ctx.bot.send_message(
            chat_id=chat_id,
            text=f"⏱ Please wait {wait}s before your next prediction.",
            reply_markup=back_keyboard()
        )

    user_last[uid] = now

    # Determine Big/Small by even/odd minute
    purchase = "Big" if now.minute % 2 == 0 else "Small"
    image    = IMAGE_BIG if purchase == "Big" else IMAGE_SMALL

    # Random colour and two numbers
    colour = random.choice(["Green", "Violet"])
    n1, n2 = random.sample(range(1, 10), 2)

    # Period: fixed prefix + 3 random digits
    prefix = "20250805100011"
    suffix = "".join(random.choices("0123456789", k=3))
    period = prefix + suffix

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

    # Send a new photo message with back button
    await ctx.bot.send_photo(
        chat_id=chat_id,
        photo=image,
        caption=caption,
        reply_markup=back_keyboard()
    )

# ── ENTRY POINT ──────────────────────────────────────────────────────────
def main():
    # 1) Start FastAPI in background thread
    threading.Thread(
        target=lambda: uvicorn.run(web, host="0.0.0.0", port=int(os.environ.get("PORT", 10000))),
        daemon=True
    ).start()

    # 2) Build and run the Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start, pattern="back"))
    app.add_handler(CallbackQueryHandler(get_prediction, pattern="get"))
    # drop pending updates and skip old ones
    app.run_polling(drop_pending_updates=True, skip_updates=True)

if __name__ == "__main__":
    main()
