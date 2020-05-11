import tweepy
import sys
import time

auth = tweepy.OAuthHandler('<consumer_key>', '<consumer_secret>')
auth.set_access_token('<access_token>', '<access_token_secret>')

api = tweepy.API(auth)
user = api.me()


def limit_handle(cursor):
    # Function to handle the Twitter API rate limit
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(300)


for follower in limit_handle(tweepy.Cursor(api.followers).items()):
    follower.follow()
    print(f'{follower.name} followed!')

search = sys.argv[1]
numberOfTweets = int(sys.argv[2])

for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
    try:
        tweet.favorite()
        print('Liked the tweet!')
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
