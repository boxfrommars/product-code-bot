import logging
import os

from telegram.ext import Updater, CommandHandler

import commands

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=os.environ.get('TOKEN'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", commands.start))
    dispatcher.add_handler(CommandHandler("help", commands.help_command))
    dispatcher.add_handler(CommandHandler("code", commands.register_code_command))
    dispatcher.add_handler(CommandHandler("codes", commands.show_codes_command))
    dispatcher.add_handler(CommandHandler("dump", commands.dump_codes_csv))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
