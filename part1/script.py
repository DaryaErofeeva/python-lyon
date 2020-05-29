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


def sep(text):
    if text[:1] == '.':
        return ' '
    else:
        return '. '


def format_doc(title, body):
    return "{}{}{}".format(title, sep(title), body).replace("\n", " ")


def remove_short(docs):
    return list(filter(lambda doc: len(doc) > 100, docs))


def remove_empty_words(words):
    return list(filter(lambda word: any(c.isalpha() for c in word), words))


def words_count(doc):
    return len(doc.split(' '))


def phrases_count(doc):
    return len(doc.split('.'))


def join_docs(docs):
    return ''.join(['{}{}'.format(doc, sep(doc)) for doc in docs])


if __name__ == "__main__":
    docs = reddit_posts() + arxiv_posts()
    docs = remove_short(docs)
    print(*docs, sep="\n")

    wc = [words_count(doc) for doc in docs]
    print('\nWords count: {}'.format(wc))
    print('Total words count: {}'.format(sum(wc)))

    pc = [phrases_count(doc) for doc in docs]
    print('\nPhrases count: {}'.format(pc))
    print('Total phrases count: {}'.format(sum(pc)))

    print('Joined text:\n{}'.format(join_docs(docs)))
