import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

# 🔑 ВАЖНО: токен теперь берётся из Railway Variables
TOKEN = os.getenv("8602440281:AAFVx5FZz81YxYgEw-rinPZEZKGQeuhlbzM")
print("TOKEN DEBUG:", repr(TOKEN))


async def is_admin(update, context):
    chat = update.effective_chat
    user_id = update.effective_user.id

    member = await context.bot.get_chat_member(chat.id, user_id)
    return member.status in ("administrator", "creator")


async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message or not message.text:
        return

    # админы не фильтруются
    async def is_admin(update, context):
    try:
        chat = update.effective_chat
        user_id = update.effective_user.id

        member = await context.bot.get_chat_member(chat.id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        print("ADMIN ERROR:", e)
        return False

    text_lower = message.text.lower()

    banned = [
        "сбор", "донат", "перевод", "карта",
        "qiwi", "paypal", "usdt", "btc",
        "http://", "https://", "t.me/"
    ]

    for word in banned:
    if word in text_lower:
        try:
            await message.delete()
        except Exception as e:
            print("DELETE ERROR (banned):", e)
        return

    if re.search(r"\b\d{16}\b", message.text) or re.search(r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", message.text):
        try:
            await message.delete()
        except Exception as e:
            print("DELETE ERROR (card):", e)
        return


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
