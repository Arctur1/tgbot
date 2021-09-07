import database as db
from settings import ALLOWED_USERS, TOKEN
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user.id
    if user in ALLOWED_USERS:
        context.job_queue.run_repeating(callback_minute, interval=10, first=1,
                                        context={"chat": update.message.chat_id, "user": user})


def stop(update: Update, context: CallbackContext) -> None:
    context.job_queue.stop()


def callback_minute(context):
    message = db.find_posts(context.job.context["user"])
    db.time_stamp(context.job.context["user"])
    context.bot.send_message(chat_id=context.job.context["chat"],
                             text=message)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('/start - подписаться\n/stop - отписаться\n/show - кол-во записей в бд')


def show(update: Update, context: CallbackContext):
    if update.effective_user.id in ALLOWED_USERS:
        message = db.count()
        update.message.reply_text(message)


def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("show", show))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
