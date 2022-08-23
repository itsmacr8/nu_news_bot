from flask import Flask
from nu_bot._nu_news_bot import NUNewsBot
from nu_bot._received_news import prev_headings, prev_links


app = Flask(__name__)


@app.route('/')
def home():
    return 'Success'


@app.route('/nu-bot')
def nu_bot():
    nu_news_bot = NUNewsBot(prev_headings, prev_links)
    nu_news_bot.init()
    nu_news_bot.add_new_news('nu_bot/_received_news.py')
    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
