import os
import urllib.request
import praw
import xmltodict

from part3.document import RedditDocument, ArxivDocument

DEFAULT_THEME = 'Minecraft'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')


class DocumentsFactory:
    @staticmethod
    def reddit_documents(theme=DEFAULT_THEME, limit=10):
        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                             user_agent=REDDIT_USER_AGENT)
        subreddit = reddit.subreddit(theme)
        return [RedditDocument(post) for post in subreddit.new(limit=limit)]

    @staticmethod
    def arxiv_documents(theme=DEFAULT_THEME, limit=10):
        url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(theme, limit)
        data = urllib.request.urlopen(url).read()
        return [ArxivDocument(entry) for entry in xmltodict.parse(data)['feed']['entry']]

    @staticmethod
    def create_documents(theme=DEFAULT_THEME, limit=10):
        return DocumentsFactory.reddit_documents(theme, limit) + DocumentsFactory.arxiv_documents(theme, limit)
