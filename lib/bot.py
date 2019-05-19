import json
import logging
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from logging import INFO
from config import APP_URL

logging.basicConfig(
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
  level=INFO
)

class HCaptchaBot(Updater):
  def add_restrictions(self, bot, update):
    """
    Iterate over newly joined chat users and for each user: restrict them and send the hcaptcha link
    """
    message = update.message
    for user in message.new_chat_members:
      # Don't welcome yourself
      if user.id == bot.id:
        continue

      logging.info(f"New user joined. chat_id: {message.chat_id}, id: {user.id}, username: {user.username}")

      logging.info('Restricting...')
      bot.restrict_chat_member(
        message.chat_id, user.id,
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
      )

      logging.info('Sending captcha...')
      bot.send_message(
        message.chat_id,
        f"**Welcome {user.name}! Please click the following link to verify yourself before you're allowed to chat.**",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=json.dumps({"inline_keyboard": [[{
          "text": "Go to verification page",
          "url": f"{APP_URL}/{message.chat_id}/{user.id}/{user.name}"
        }]]})
      )

  def remove_restrictions(self, chat_id, user_id, user_name):
    """
    Remove chat restrictions for `user_id` then notify them
    """
    bot = self.bot

    logging.info(f"User is human. username: {user_name}, id: {user_id}")

    logging.info('Removing restctions...')
    bot.restrict_chat_member(
      chat_id, user_id,
      can_send_messages=True,
      can_send_media_messages=True,
      can_send_other_messages=True,
    )

    logging.info('Sending notification...')
    bot.send_message(
      chat_id,
      f"**Thanks {user_name}! You are now allowed to chat.**",
      parse_mode=ParseMode.MARKDOWN,
    )

  def add_handlers(self):
    logging.info('Adding handlers...')
    self.dispatcher.add_handler(
      MessageHandler(Filters.status_update.new_chat_members, self.add_restrictions)
    )

  def run(self):
    self.add_handlers()

    # TODO: use webhooks on production. Currently using polling for ease of development and deployment.
    self.start_polling()
    logging.info('Polling...')

    self.idle()
