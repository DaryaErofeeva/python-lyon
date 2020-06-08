import os
import urllib.request
import praw
import xmltodict

from part34.document import RedditDocument, ArxivDocument

DEFAULT_THEME = 'Minecraft'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')


class DocumentsFactory:
    """
    3.5
    """
    @staticmethod
    def reddit_documents(theme=DEFAULT_THEME, limit=10):
        reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
                             user_agent=REDDIT_USER_AGENT)
        subreddit = reddit.subreddit(theme)
        filtered_posts = list(filter(lambda post: len(post.selftext) > 100, subreddit.new(limit=limit)))
        return [RedditDocument(post) for post in filtered_posts]

    @staticmethod
    def arxiv_documents(theme=DEFAULT_THEME, limit=10):
        url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(theme, limit)
        data = urllib.request.urlopen(url).read()
        parsed_data = xmltodict.parse(data)
        filtered_entries = list(filter(lambda entry: len(entry['summary']) > 100, parsed_data['feed']['entry']))
        return [ArxivDocument(entry) for entry in filtered_entries]

    @staticmethod
    def create_documents(theme=DEFAULT_THEME, limit=10):
        return DocumentsFactory.reddit_documents(theme, limit) + DocumentsFactory.arxiv_documents(theme, limit)
