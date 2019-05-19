import urllib.request
import urllib.parse
import json
from flask import Flask, render_template, request
from lib.bot import HCaptchaBot
from config import TELEGRAM_TOKEN, HCAPTCHA_SECRET, HCAPTCHA_POST_URI, HCAPTCHA_SITE_KEY

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/<chat_id>/<user_id>/<user_name>")
def captcha(chat_id=None, user_id=None, user_name=None):
  return render_template(
    "captcha.html",
    chat_id=chat_id, user_id=user_id, user_name=user_name, site_key=HCAPTCHA_SITE_KEY
  )

@app.route("/<chat_id>/<user_id>/<user_name>/verify", methods=['POST'])
def verify(chat_id=None, user_id=None, user_name=None):
  token = request.form["h-captcha-response"]
  params = urllib.parse.urlencode({
    "secret": HCAPTCHA_SECRET,
    "response": token
  })

  with urllib.request.urlopen(HCAPTCHA_POST_URI, params.encode("ascii")) as response:
    json_response = json.loads(response.read().decode("utf-8"))

    if json_response["success"]:
      HCaptchaBot(TELEGRAM_TOKEN).remove_restrictions(chat_id, user_id, user_name)

      return render_template("success.html")
    else:
      return render_template("error.html")

if __name__ == "__main__":
  app.run()
