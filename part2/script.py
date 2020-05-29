import pickle
from datetime import datetime
import os
import praw
import urllib.request
import xmltodict
from part2.corpus import Corpus

DEFAULT_THEME = 'Minecraft'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

ARXIV_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


class Document:
    """
    title - title
    author - author(s) name(s)
    date - publication date
    url - source url
    text - content text
    """

    def __init__(self, title, author, date, url, text):
        self.title = title.replace("\n", " ")
        self.author = author
        self.date = date
        self.url = url
        self.text = text.replace("\n", " ")

    def __str__(self):
        return '\nTitle: {}\nAuthor: {}\nDate: {}\nUrl: {}'.format(self.title, self.author, self.date, self.url)

    def print(self):
        print(self)


class Author:
    """
    name - name
    ndoc - docs count
    publications - dictionary of publications
    """

    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.publications = {}

    def add(self, publication: Document):
        self.publications[self.ndoc] = publication
        self.ndoc += 1

    def __str__(self):
        publications_names = [doc.title for doc in self.publications.values()]
        return '\n\nAuthor {} has following publications: \n{}'.format(self.name, '\n\t'.join(publications_names))

    def __eq__(self, other):
        return self.name == other.name


def unix_time_to_date(unix_time):
    return datetime.fromtimestamp(unix_time)


def reddit_post_to_doc(post):
    return Document(post.title, post.author.name, unix_time_to_date(post.created_utc), post.url, post.selftext)


def reddit_posts(theme=DEFAULT_THEME, limit=10):
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)
    subreddit = reddit.subreddit(theme)
    return [reddit_post_to_doc(post) for post in subreddit.new(limit=limit)]


def parse_arxiv_date(date):
    return datetime.strptime(date, ARXIV_DATE_FORMAT)


def arxiv_entry_to_doc(entry):
    author = entry['author']
    if type(author) is list:
        author = ', '.join([a['name'] for a in author])
    else:
        author = author['name']
    date = parse_arxiv_date(entry['published'])
    return Document(entry['title'], author, date, entry['id'], entry['summary'])


def arxiv_posts(theme=DEFAULT_THEME, limit=10):
    url = 'http://export.arxiv.org/api/query?search_query=all:{}&start=0&max_results={}'.format(theme, limit)
    data = urllib.request.urlopen(url).read()
    return [arxiv_entry_to_doc(entry) for entry in xmltodict.parse(data)['feed']['entry']]


if __name__ == "__main__":
    docs = reddit_posts() + arxiv_posts()

    collection = {}  # alternative way {i: docs[i] for i in range(len(docs))}
    authors = {}
    for index in range(len(docs)):
        collection[index] = docs[index]
        names = docs[index].author.split(', ')
        for name in names:
            author = Author(name)
            try:
                author_index = list(authors.values()).index(author)
                authors[author_index].add(docs[index])
            except ValueError:
                author.add(docs[index])
                authors[len(authors)] = author

    id2doc = {key: value.title for key, value in collection.items()}
    print(id2doc)

    id2aut = {key: value.name for key, value in authors.items()}
    print(id2aut)

    corpus = Corpus('Corpus', authors, id2aut, collection, id2doc, len(collection), len(authors))
    print(corpus.print())

    print('\n\nSerializing corpus...')
    corpus.save()
    print('Corpus serialized')
    print('Removing corpus instance...')
    del corpus
    print('Corpus instance removed')
    print('Deserializing corpus')
    with open('data.pickle', 'rb') as f:
        corpus = pickle.load(f)
    print('Corpus deserialized')
    corpus.print()
