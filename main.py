from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import datetime

# Your actual bot token
BOT_TOKEN = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"

# Final working direct image links
IMAGE_BIG = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"

def get_prediction_type():
    return "Big" if datetime.datetime.utcnow().minute % 2 == 0 else "Small"

def generate_period():
    base = "2025080510001"
    ending = ''.join(random.choices("0123456789", k=4))
    return base + ending

def get_random_colour():
    return random.choice(["Red", "Violet"])

def get_random_numbers():
    nums = random.sample(range(1, 10), 2)
    return f"{nums[0]} or {nums[1]}"

def build_prediction_text(purchase: str):
    return (
        "🎰 *Prediction for winGO 1 MIN* 🎰\n\n"
        f"📅 *Period:* {generate_period()}\n"
        f"💸 *Purchase:* {purchase}\n\n"
        f"🔮 *Risky Predictions:*\n"
        f"👉🏻 *Colour:* {get_random_colour()}\n"
        f"👉🏻 *Numbers:* {get_random_numbers()}\n\n"
        f"💡 *Strategy Tip:*\n"
        f"Use the 2x strategy for better chances of profit and winning.\n\n"
        f"📊 *Fund Management:*\n"
        f"Always play through fund management 5 level."
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "User"
    username = f"@{user.username}" if user.username else "N/A"
    user_id = user.id

    welcome = (
        f"🌟 Welcome, {name}! 🌟\n"
        f"👤 Username: {username}\n"
        f"🆔 User ID: {user_id}\n\n"
        "Please select an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="get_prediction")],
        [
            InlineKeyboardButton("🔗 Register Link", url="https://www.tashanwin.ink/#/register?invitationCode=344522232221"),
            InlineKeyboardButton("📢 Prediction Channel", url="https://t.me/+RNUQHXvEy5w0ZDk1")
        ]
    ]

    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "get_prediction":
        prediction_type = get_prediction_type()
        photo_url = IMAGE_BIG if prediction_type == "Big" else IMAGE_SMALL
        caption = build_prediction_text(prediction_type)
        await query.message.reply_photo(photo=photo_url, caption=caption, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
