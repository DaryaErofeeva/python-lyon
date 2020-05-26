import os
import praw
import urllib.request
import xmltodict

DEFAULT_THEME = 'Minecraft'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')


def reddit_posts(theme=DEFAULT_THEME, limit=10):
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)
    subreddit = reddit.subreddit(theme)
    return [format_doc(post.title, post.selftext) for post in subreddit.new(limit=limit)]


def arxiv_posts(theme=DEFAULT_THEME, limit=10):
    url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(theme, limit)
    data = urllib.request.urlopen(url).read()
    return [format_doc(entry['title'], entry['summary']) for entry in xmltodict.parse(data)['feed']['entry']]


def format_doc(title, body):
    return "{} : {}".format(title, body).replace("\n", " ")


if __name__ == "__main__":
    docs = reddit_posts() + arxiv_posts()
    print(*docs, sep="\n")
