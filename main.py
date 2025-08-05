import random
from datetime import datetime, timedelta
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ── CONFIG ────────────────────────────────────────────────────────────────

BOT_TOKEN        = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"
IMAGE_BIG        = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL      = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"
REGISTER_LINK    = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHNL  = "https://t.me/+RNUQHXvEy5w0ZDk1"
STICKER_FILE_ID  = "CAACAgUAAxkBAAEEj_xljozTcFd1wHEwUCDj9JPlKQxh0wACaAoAAj-VQUV9d0AXc5UX1zQE"

# ── PER-USER COOLDOWN TRACKER ──────────────────────────────────────────────

user_last_prediction: dict[int, datetime] = {}

# ── BUILD MAIN MENU ───────────────────────────────────────────────────────

def build_main_menu():
    return InlineKeyboardMarkup([
        # Top row: Get Prediction
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get_prediction")],
        # Second row: Register & Channel side by side
        [
            InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHNL)
        ]
    ])

# ── /start HANDLER ─────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = (
        f"🌟 Welcome, {user.first_name}! 🌟\n"
        f"👤 Username: @{(user.username or 'N/A')}\n"
        f"🆔 User ID: {user.id}\n\n"
        "Please select an option below:"
    )
    await update.message.reply_text(
        welcome,
        reply_markup=build_main_menu()
    )

# ── PREDICTION HANDLER ─────────────────────────────────────────────────────

async def get_prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    now = datetime.utcnow()
    last = user_last_prediction.get(uid)
    if last and (now - last) < timedelta(seconds=60):
        wait = 60 - int((now - last).total_seconds())
        return await query.edit_message_text(f"⏱ Please wait {wait}s before requesting another prediction.")

    # update last-request time
    user_last_prediction[uid] = now

    # Generate prediction details
    purchase = "Big" if now.minute % 2 == 0 else "Small"
    colour   = random.choice(["Green", "Violet"])
    nums     = random.sample(range(1, 10), 2)
    number_text = f"{nums[0]} or {nums[1]}"
    period   = now.strftime("%Y%m%d%H%M")  # e.g. 202508051234
    image    = IMAGE_BIG if purchase == "Big" else IMAGE_SMALL

    caption = (
        "🎰 Prediction for Tashan Win 1 MIN 🎰\n\n"
        f"📅 Period: {period}\n"
        f"💸 Purchase: {purchase}\n\n"
        "🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {colour}\n"
        f"👉🏻 Numbers: {number_text}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    # 1) Send photo + caption + back button
    await query.edit_message_media(
        media={
            "type": "photo",
            "media": image,
            "caption": caption
        },
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_to_menu")
        ]])
    )

    # 2) Send Go! Go! Go! sticker below the prediction
    await context.bot.send_sticker(chat_id=uid, sticker=STICKER_FILE_ID)

# ── BACK TO MENU HANDLER ────────────────────────────────────────────────────

async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🏠 Main Menu", reply_markup=build_main_menu())

# ── ENTRY POINT ─────────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(get_prediction, pattern="get_prediction"))
    app.add_handler(CallbackQueryHandler(back_to_menu, pattern="back_to_menu"))

    # Blocks here, polling Telegram
    app.run_polling()

if __name__ == "__main__":
    main()
