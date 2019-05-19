from lib.bot import HCaptchaBot
from config import TELEGRAM_TOKEN

if __name__ == "__main__":
  HCaptchaBot(TELEGRAM_TOKEN).run()
