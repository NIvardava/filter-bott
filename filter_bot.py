import os
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TOKEN")


async def is_admin(update, context):
    try:
        chat = update.effective_chat
        user_id = update.effective_user.id

        member = await context.bot.get_chat_member(chat.id, user_id)
        return member.status in ("administrator", "creator")
    except Exception as e:
        print("ADMIN ERROR:", e)
        return False


async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message:
            return

        message = update.message

        if not message.text:
            return

        if await is_admin(update, context):
            return

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
                    print("DELETE ERROR:", e)
                return

        if re.search(r"(?:\d[\s-]*){16}", message.text):
            try:
                await message.delete()
            except Exception as e:
                print("DELETE ERROR:", e)
            return

    except Exception as e:
        print("GENERAL ERROR:", e)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_messages))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
