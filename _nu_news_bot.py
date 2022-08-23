import requests
import time
import os
import smtplib
from bs4 import BeautifulSoup
from ssl import create_default_context
from email.message import EmailMessage
from _received_news import prev_headings, prev_links


class NUNewsBot:
    news_headings = []
    news_links = []
    user_info = []

    def init(self):
        soup = BeautifulSoup(self.get_webpage(), 'html.parser')
        self.get_news(soup)
        self.get_recipients()
        if (self.news_headings and self.news_links):
            for user in self.user_info:
                message = self.get_message(user['name'], user['email'])
                self.send_mail(message)
                time.sleep(5)
            print('New has been sent to your email address.')
        else:
            print('No new news found.')

    def get_webpage(self):
        """Return Scrap website."""
        NU = {
            'url': 'https://www.nu.ac.bd/examination-notice.php',
            # visit http://myhttpheader.com/ to get the below information.
            'headers': {
                'User-Agent': 'Defined',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        }
        try:
            response = requests.get(
                f"{NU.get('url')}", headers=NU.get('headers'))
        except requests.exceptions.MissingSchema:
            print('The URL is not correct.')
            quit()
        else:
            web_page = response.text
        return web_page

    def get_news(self, soup):
        """
            *   Select top 10 news items from the scrap website.
            *   Store the new news heading and link to their appropriate list.
        """
        top_10_news = soup.select(selector='.news-item a')[:10]
        new_headings = []
        new_links = []
        for news in top_10_news:
            new_heading = news.getText().strip()
            new_link = f"https://www.nu.ac.bd/{news.get('href')}"
            new_headings.append(new_heading)
            new_links.append(new_link)
        self.is_new_news(new_headings, new_links)
        self.add_new_news(new_headings, new_links)

    def is_new_news(self, new_headings, new_links):
        """Update the news_headings and news_links list with the latest news that are not found in the _received_news file."""
        self.news_headings = [
            nh for nh in new_headings if nh not in prev_headings]
        self.news_links = [
            link for link in new_links if link not in prev_links]

    def add_new_news(self, new_headings, new_links):
        """Update _received_news file with the today's latest news."""
        content = f'prev_headings = {new_headings}\n\nprev_links = {new_links}'
        with open('_received_news.py', mode='w', encoding='UTF-8') as file:
            file.write(content)

    def get_recipients(self):
        """Loop over the sheet_data and add every recipient"""
        sheet_data = self.get_sheet_data()
        for user in sheet_data['userInfo']:
            self.add_user(user)

    def get_sheet_data(self):
        """Get data from the excel file."""
        SHETTY = {
            'sheet': os.environ.get('sheet_name'),
            'project': os.environ.get('project_name'),
            'code': os.environ.get('project_code'),
            'token': f"Bearer {os.environ.get('shetty_token')}",
        }
        shetty_endpoint = f"https://api.sheety.co/{SHETTY['code']}/{SHETTY['project']}/{SHETTY['sheet']}"
        headers = {'Authorization': SHETTY['token']}
        return requests.get(url=shetty_endpoint, headers=headers).json()

    def add_user(self, user):
        """Clean user provided data and add user information to the user_info list."""
        if user['name'] and user['emailAddress']:
            self.user_info.append(
                {'name': user['name'].strip(), 'email': user['emailAddress'].strip()})

    def get_message(self, recipient_name, recipient_email):
        """Set mail sender and recipient email address and structure the mail message."""
        mail = {
            'intro': f'Dear {recipient_name},\n\nআপনাকে জাতীয় বিশ্ববিদ্যালয়ের আজকের সর্বশেষ খবর জানানোর জন্য এই ইমেইলটি পাঠানো হয়েছে।',
            'body': ''.join(
                f'{news_heading}বিস্তারিত জানার জন্য নিচের লিংকে ক্লিক করুন।\n{self.news_links[num]}\n\n\n' for num, news_heading in enumerate(self.news_headings)),
        }
        message = EmailMessage()
        message['From'] = os.environ.get('sender_email')
        message['pass'] = os.environ.get('sender_password')
        message['To'] = recipient_email
        message['Subject'] = "The National University's most recent exam news as of now."
        message.set_content(f"{mail['intro']}\n\n{mail['body']}")
        return message

    def send_mail(self, msg):
        """Authenticate sender email and send the email message."""
        with smtplib.SMTP('smtp.gmail.com') as smtp:
            # Secure the connection
            smtp.starttls(context=create_default_context())
            try:
                smtp.login(user=msg['From'], password=msg['pass'])
            except smtplib.SMTPAuthenticationError as e:
                print('Authentication failed', e)
            try:
                smtp.send_message(msg)
            except smtplib.SMTPRecipientsRefused as e:
                print('Recipient refused', e)
