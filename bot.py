import os
import logging
import requests
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def send_post_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = "https://dining.iut.ac.ir/api/v0/TransferFoodBuy?mealId=2&status=123"
    headers = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        "x-xsrf-token": "by5XLH_87wNs9osbz2wcrq5t8cmDviP0h_ICGDqK9eMTh4cXH0tA_LXgxURu2X8pmYetdwDQFyKZwYzKUQapXrDQaBtbVVBwa2uFMWTejFUNN9ocsjEZQ38tsPtKf1UotWErHg2",
    }
    cookies = {
        "FirstFoodCookie": "isFirstFood=true",
        "JahangostarSetare": "VzoV1USOJO6hDaMY3dDJ_02pP-2F4JgQoICnrG6qH3LlXm...",
    }

    try:
        response = requests.post(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            await update.message.reply_text("Request sent successfully!")
        else:
            await update.message.reply_text(f"Request failed with status code {response.status_code}.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send 'REQ' to trigger the POST request.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.strip().upper() == "REQ":
        await send_post_request(update, context)
    else:
        await update.message.reply_text(update.message.text)

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
