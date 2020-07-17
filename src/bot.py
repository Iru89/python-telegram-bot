from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config.auth import token

import schedule
import time
import threading

import logging
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('DailyIskraBot')


def start(update, context):
    logger.info('He rebut un comando start')
    user = update.message.chat.first_name
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hola {user}, soc @DailyIskraBot i la meva funcio es gestionar la informacio de la daily cada dia")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def daily(update, context):
    try:
        date = datetime.datetime.now()

        projecte = context.args[0]

        descripcio = context.args.pop(0)
        descripcio = " ".join(context.args)

        logger.info(
            f"{date} projecte: {projecte} descripcio: {descripcio}")

        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Registrat")
    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="La comanda no es correcte")


def alarma(update, context):
    logger.info(context.args)

    try:
        hour = context.args.pop(0)
        minutes = context.args.pop(0)
        days = context.args.pop(0)
        message = " ".join(context.args)

        # schedule.every(days).days.at(f"{hour}:{minutes}").do(message)
        schedule.every(1).minutes.do(run_threaded, remainder, context,
                                     update.effective_chat.id, message)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="La comanda no es correcte")


def remainder(context, chat_id, message):
    context.bot.send_message(chat_id=chat_id, text=message)


def run_threaded(job_func, context, chat_id, message):
    job_thread = threading.Thread(
        target=job_func, args=[context, chat_id, message])
    job_thread.start()


# def pending():
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


if __name__ == '__main__':

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    alarma_handler = CommandHandler('alarma', alarma)
    dispatcher.add_handler(alarma_handler)

    daily_handler = CommandHandler('daily', daily)
    dispatcher.add_handler(daily_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    # pending_thread = threading.Thread(target=pending)
    # pending_thread.start()

    updater.start_polling()
    updater.idle()
