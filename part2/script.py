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

PICKLE_FILE_NAME = 'data.pickle'


class Document:
    """
    2.1
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
    2.4
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
    filtered_posts = list(filter(lambda post: len(post.selftext) > 100, subreddit.new(limit=limit)))
    return [reddit_post_to_doc(post) for post in filtered_posts]


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
    parsed_data = xmltodict.parse(data)
    filtered_entries = list(filter(lambda entry: len(entry['summary']) > 100, parsed_data['feed']['entry']))
    return [arxiv_entry_to_doc(entry) for entry in filtered_entries]


if __name__ == "__main__":
    print('\n+++++++++++++++++++++++ PART 2 +++++++++++++++++++++++')

    print('====================== 2.1 | 2.2 ======================')
    print(Document('test title', 'test author', datetime.now(), 'http://test_url', 'test text'))

    print('\n========================= 2.3 =========================')

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
    for key, value in collection.items():
        print("{}, {}".format(key, value))

    id2doc = {key: value.title for key, value in collection.items()}
    for key, value in id2doc.items():
        print("{}, {}".format(key, value))

    print('\n=================== 2.4 | 2.5 | 2.6 ===================')
    for key, value in authors.items():
        print("{}, {}".format(key, value))

    id2aut = {key: value.name for key, value in authors.items()}
    for key, value in id2aut.items():
        print("{}, {}".format(key, value))

    print('\n====================== 2.7 | 2.8 ======================')
    corpus = Corpus('Corpus', authors, id2aut, collection, id2doc, len(collection), len(authors))
    print('----------------------- __repr__ ----------------------')
    print(corpus.__repr__())
    print('Afficher les élément du corpus triés selon la date et le titre')
    print(corpus.print())

    print('\n========================= 2.9 =========================')
    print('Serializing corpus...')
    corpus.save(PICKLE_FILE_NAME)
    print('Corpus serialized')
    print('Removing corpus instance...')
    del corpus
    print('Corpus instance removed')
    print('Deserializing corpus')
    with open(PICKLE_FILE_NAME, 'rb') as f:
        corpus = pickle.load(f)
    print('Corpus deserialized')
    corpus.print()
