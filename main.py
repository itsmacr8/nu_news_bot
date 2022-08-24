from flask import Flask, render_template
from nu_bot._nu_news_bot import NUBot
from nu_bot._received_news import prev_headings, prev_links
from utils import write_bot_status


app = Flask(__name__)


@app.route('/')
def home():
    from nu_bot._status import bot_info
    return render_template('index.html', bot=bot_info)


@app.route('/nu-bot')
def nu_bot():
    nu_bot = NUBot(prev_headings, prev_links)
    nu_bot.init()
    write_bot_status('nu_bot/_status.py', f'{nu_bot.get_bot_info()}')
    nu_bot.add_new_news('nu_bot/_received_news.py')
    return 'Success'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
