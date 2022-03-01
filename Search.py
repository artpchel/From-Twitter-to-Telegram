from config import create_api
import tweepy
import logging
import telebot
from queue import Queue
from threading import Thread
import time

bot = telebot.TeleBot('1819299619:AAHVNcVvOxHHMZm-qwnDHdve8fFSB9gkLCw')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, q = Queue()):

        self.api = api
        self.me = api.me()

        num_worker_threads = 4
        self.q = q
        for i in range(num_worker_threads):
            t = Thread(target=self.do_stuff)
            t.daemon = True
            t.start()

    def on_limit(self, status):
        print("Rate Limit Exceeded, Sleep for 15 Mins")
        time.sleep(15 * 60)
        return True

    def on_status(self, tweet):
        if "@gmail.com" in tweet.text:
            bot.send_message(chat_id = '270834635', text = str(tweet.user.name) + "" + str(tweet.text))

    def on_error(self, status):
        logger.error(status)
        if status == 420:
            # returning False in on_data disconnects the stream
            return False

    def do_stuff(self):
        while True:
            self.q.get()
            self.q.task_done()


def main(keywords):
    api = create_api()
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])



if __name__ == "__main__":
    main(["Send me loops", "send loops", "send melodic loops", "send melodic starters", "send midi", "send midis", "send me midi"])
