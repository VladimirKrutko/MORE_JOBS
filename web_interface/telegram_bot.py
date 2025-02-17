from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from web_interface.llm_model_interface import LLMModelInterface
from scripting.loader.models.offer import Offer, Session
from telegram import Update
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send me a message and I'll get a response from the model.")

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text
    try:
        response = LLMModelInterface.get_response_according_chromadb(user_text)
        message_text = response['llm_text'] + "\n" + offer_urls([ int(id) for id in response['ids'][0]])
        await update.message.reply_text(message_text)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

def offer_urls(ids):
    session = Session()
    urls = session.query(Offer.url).filter(Offer.id.in_(ids)).all()
    session.close()
    return "\n".join([url[0] for url in urls])


def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
