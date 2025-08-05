from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
from datetime import datetime, timezone, timedelta
from flask import Flask
import threading

# ── CONFIG ─────────────────────────────────────────────────────────────

BOT_TOKEN = "7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI"

IMAGE_BIG = "https://i.ibb.co/VczDcfgC/6282730971962918809.jpg"
IMAGE_SMALL = "https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg"

REGISTER_LINK      = "https://www.tashanwin.ink/#/register?invitationCode=344522232221"
PREDICTION_CHANNEL = "https://t.me/+RNUQHXvEy5w0ZDk1"

# ── GLOBAL STATE ────────────────────────────────────────────────────────

_last_gen_time: datetime | None = None
_current_prediction: dict = {}

# ── PREDICTION GENERATOR ─────────────────────────────────────────────────

def _generate_prediction():
    """Regenerates global prediction data."""
    purchase = "Big" if random.choice([True, False]) else "Small"
    colour   = random.choice(["Green", "Violet"])
    nums     = random.sample(range(0, 10), 2)
    period   = "2025080510001" + "".join(random.choices("0123456789", k=4))

    image_url = IMAGE_BIG if purchase == "Big" else IMAGE_SMALL

    caption = (
        "🎰 *Prediction for winGO 1 MIN* 🎰\n\n"
        f"📅 *Period:* {period}\n"
        f"💸 *Purchase:* {purchase}\n\n"
        f"🔮 *Risky Predictions:*\n"
        f"👉🏻 *Colour:* {colour}\n"
        f"👉🏻 *Numbers:* {nums[0]} or {nums[1]}\n\n"
        f"💡 *Strategy Tip:*\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        f"📊 *Fund Management:*\n"
        "Always play through fund management 5 level."
    )

    return {
        "time": datetime.now(timezone.utc),
        "image_url": image_url,
        "caption": caption
    }

def get_prediction():
    global _last_gen_time, _current_prediction

    now = datetime.now(timezone.utc)
    # First time or older than 60s → regenerate
    if _last_gen_time is None or (now - _last_gen_time) >= timedelta(seconds=60):
        _current_prediction = _generate_prediction()
        _last_gen_time = _current_prediction["time"]

    return _current_prediction["image_url"], _current_prediction["caption"]

# ── HANDLERS ────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "User"
    uid  = user.id

    welcome = (
        f"🌟 Welcome, {name}! 🌟\n"
        f"👤 Username: @{user.username if user.username else 'N/A'}\n"
        f"🆔 User ID: {uid}\n\n"
        "Please select an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="predict")],
        [
            InlineKeyboardButton("🔗 Register Link",      url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=PREDICTION_CHANNEL)
        ]
    ]

    await update.message.reply_text(
        welcome,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    image_url, caption = get_prediction()
    await query.message.reply_photo(photo=image_url, caption=caption, parse_mode="Markdown")

# ── FLASK SERVER FOR RENDER ─────────────────────────────────────────────

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return "✅ Telegram bot is running."

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

# ── MAIN ─────────────────────────────────────────────────────────────────

def main():
    # Start the Telegram bot in a separate thread
    def run_bot():
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_predict, pattern="predict"))
        app.run_polling()

    threading.Thread(target=run_bot).start()

    # Run the Flask server (so Render sees an open port)
    run_flask()

if __name__ == "__main__":
    main()
