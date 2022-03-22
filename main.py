import logging
import os
from os.path import join, dirname

from dotenv import load_dotenv
from sqlalchemy import create_engine, text, insert
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(os.environ.get('SQLALCHEMY_URL'), echo=True)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def register_code_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if len(context.args) < 1:
        update.message.reply_text('Укажите код')
    else:
        code = str(context.args[0])
        user = update.message.from_user

        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO codes (user_id, username, first_name, last_name, code) "
                     "VALUES (:user_id, :username, :first_name, :last_name, :code)"),
                [{
                    'user_id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    "code": code
                }])

        update.message.reply_text(f'Код {code} принят')


def show_codes_command(update: Update, context: CallbackContext) -> None:

    with engine.connect() as conn:
        result = conn.execute(text("select * from codes"))
        message = ''
        for row in result:
            message += f"code: {row['code']}\n"

    update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=os.environ.get('TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("code", register_code_command))
    dispatcher.add_handler(CommandHandler("codes", show_codes_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
