import os

import csv
import pytz
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
from itertools import groupby
import messages as msg
from sqlalchemy import create_engine, text
from telegram import Update
from telegram.ext import CallbackContext

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

engine = create_engine(os.environ.get('SQLALCHEMY_URL'), echo=True)


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(msg.greet())


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(msg.help_message())


def register_code_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if len(context.args) < 1:
        update.message.reply_text(msg.empty_code())

        return

    code = str(context.args[0]).strip().upper()
    if not len(code):
        update.message.reply_text(msg.empty_code())

        return

    code_type = code[0]

    if not code_type.isalpha():
        update.message.reply_text(msg.invalid_code(code))

        return

    user = update.message.from_user

    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO codes (user_id, username, first_name, last_name, code_type, code) "
                 "VALUES (:user_id, :username, :first_name, :last_name, :code_type, :code)"),
            [{
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                "code_type": code_type,
                "code": code
            }])

    update.message.reply_text(msg.code_added(code))


def show_codes_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM codes WHERE username = :username"),
                              {'username': user.username})
        message = ''
        for row in result:
            message += f"code: {row['code']}\n"

    update.message.reply_text(message)


def dump_codes_csv(update: Update, context: CallbackContext) -> None:
    fieldnames = ['id', 'added_at', 'user_id', 'username', 'first_name', 'last_name', 'code_type', 'code']

    tz_source = pytz.timezone('UTC')
    tz_target = pytz.timezone('Europe/Moscow')

    current_date = datetime.now(tz_target).strftime('%Y-%m-%d')

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM codes"))

        rows = [dict(r) for r in result.fetchall()]

        for row in rows:
            row['added_at'] = tz_source.localize(parser.parse(row['added_at'])).astimezone(tz_target)

    for code_type, codes in groupby(rows, key=lambda x: x['code_type']):
        filename = f'codes-{code_type}-{current_date}.csv'
        with open(f'../{filename}', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(codes)

        with open(f'../{filename}', 'rb') as f:
            update.message.reply_document(document=f, filename=filename)


def wipe(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('OK!')
