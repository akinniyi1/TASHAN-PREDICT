from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import datetime

# BOT CONFIG
BOT_TOKEN = '7665990129:AAGJ2wCzzJhgmb2OGRc5kn8XdfKCh2CUqlI'
REGISTER_LINK = 'https://www.tashanwin.ink/#/register?invitationCode=344522232221'
CHANNEL_LINK = 'https://t.me/+RNUQHXvEy5w0ZDk1'
IMAGE_BIG = 'https://i.ibb.co/VczDcfgC/6282730971962918809.jpg'
IMAGE_SMALL = 'https://i.ibb.co/qMsTSbG8/6282730971962918811.jpg'
STICKER_ID = 'CAACAgEAAxkBAAIBG2Ymt9yS_VUbZu8Y5w6vlsfKRE9QAAKPAwACUkt5RzyIsyP8dOdwNQQ'  # Go! Go! Go!

# COMMAND: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name
    user_id = user.id

    keyboard = [
        [InlineKeyboardButton("🔮 Get Prediction", callback_data="predict")],
        [
            InlineKeyboardButton("🔗 Register Link", url=REGISTER_LINK),
            InlineKeyboardButton("📢 Prediction Channel", url=CHANNEL_LINK)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Hello {name} (ID: {user_id})\nWelcome to the winGO 1 MIN Prediction Bot!\n\nChoose an option below:",
        reply_markup=reply_markup
    )

# CALLBACK: Menu handler
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "predict":
        await send_prediction(query, context)

    elif query.data == "back":
        await start(update, context)

# GENERATE AND SEND PREDICTION
async def send_prediction(query, context):
    # Toggle logic
    toggle = random.choice(["BIG", "SMALL"])
    image = IMAGE_BIG if toggle == "BIG" else IMAGE_SMALL
    color = random.choice(["Green", "Red", "Blue"])
    numbers = random.sample(range(0, 10), 2)

    # Period format
    now = datetime.datetime.now()
    period = now.strftime("%Y%m%d%H%M")

    # Message
    message = (
        "🎰 Prediction for winGO 1 MIN 🎰\n\n"
        f"📅 Period: {period}\n"
        f"💸 Purchase: {toggle}\n"
        f"🔮 Risky Predictions:\n"
        f"👉🏻 Colour: {color}\n"
        f"👉🏻 Numbers: {numbers[0]} or {numbers[1]}\n\n"
        "💡 Strategy Tip:\n"
        "Use the 2x strategy for better chances of profit and winning.\n\n"
        "📊 Fund Management:\n"
        "Always play through fund management 5 level."
    )

    # Back to Menu button
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send image + prediction
    await query.message.reply_photo(photo=image, caption=message, reply_markup=reply_markup)

    # Send sticker
    await context.bot.send_sticker(chat_id=query.message.chat_id, sticker=STICKER_ID)

# RUN BOT
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()
