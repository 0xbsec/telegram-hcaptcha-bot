import unittest
from telegram import Update, Chat, Message, User
from unittest.mock import MagicMock
from lib.bot import HCaptchaBot
from config import TELEGRAM_TOKEN, TELEGRAM_USERNAME

class TestGetMe(unittest.TestCase):
  bot = HCaptchaBot(TELEGRAM_TOKEN).bot
  bot_info = bot.get_me()

  def test_is_bot(self):
    self.assertTrue(TestGetMe.bot_info['is_bot'])

  def test_username(self):
    self.assertEqual(TestGetMe.bot_info['username'], TELEGRAM_USERNAME)

class TestBotUpdates(unittest.TestCase):
  def _fetch_updates(self, bot):
    chat = Chat(
      id=1,
      type='private',
      first_name='Joe',
      last_name='Doe'
    )
    user = User(
      id=1,
      first_name='Joe',
      last_name='Doe',
      is_bot=False,
    )
    return [
      Update(
        update_id=1,
        message=Message(
          message_id=1,
          chat=chat,
          date=None,
          from_user=user,
          bot=bot,
        )
      ),
      Update(
        update_id=2,
        message=Message(
          message_id=7,
          date=None,
          chat=chat,
          new_chat_members=[user],
          from_user=user,
          bot=bot,
        )
      )
    ]

  def test_restrict(self):
    updater = HCaptchaBot(TELEGRAM_TOKEN)
    bot = updater.bot

    # mock start_polling()
    bot.get_updates = MagicMock(return_value=self._fetch_updates(bot))
    update_event = bot.get_updates().pop(1)

    bot.get_updates.assert_called()

    # mock add_restrictions
    bot.restrict_chat_member = MagicMock(return_value=None)
    bot.send_message = MagicMock(return_value=None)
    updater.add_restrictions(bot, update_event)

    bot.restrict_chat_member.assert_called()
    bot.send_message.assert_called()

    # mock remove_restrictions
    updater.remove_restrictions(
      update_event.message.chat.id,
      update_event.message.from_user.id,
      update_event.message.from_user.name,
    )

    bot.restrict_chat_member.assert_called()
    bot.send_message.assert_called()

if __name__ == '__main__':
  unittest.main()
