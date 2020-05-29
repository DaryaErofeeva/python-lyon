from collections import OrderedDict

from praw.reddit import Submission
from part2.script import unix_time_to_date, parse_arxiv_date


class Document:
    """
    title - title
    author - author(s) name(s)
    date - publication date
    url - source url
    text - content text
    """

    def __init__(self, title, author, date, url, text):
        self.__title = title.replace("\n", " ")
        self.__author = author
        self.__date = date
        self.__url = url
        self.__text = text.replace("\n", " ")

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_author(self):
        return self.__author

    def set_author(self, author):
        self.__author = author

    def get_date(self):
        return self.__date

    def set_date(self, date):
        self.__date = date

    def get_url(self):
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_text(self):
        return self.__text

    def set_text(self, text):
        self.__text = text

    def get_type(self):
        pass

    def __str__(self):
        return '\nTitle: {}\nAuthor: {}\nDate: {}\nUrl: {}\nSource: {}' \
            .format(self.__title, self.__author, self.__date, self.__url, self.get_type())

    def print(self):
        print(self)


class RedditDocument(Document):
    """
    Additional fields:
    edited - whether or not the submission has been edited
    score - the number of upvotes for the submission
    """

    def __init__(self, post: Submission):
        super().__init__(post.title, post.author.name, unix_time_to_date(post.created_utc), post.url, post.selftext)
        self.__edited = post.edited
        self.__score = post.score

    def get_edited(self):
        return self.__edited

    def set_edited(self, edited):
        self.__edited = edited

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score

    def get_type(self):
        return 'Reddit'

    def __str__(self):
        return '{}\nEdited: {}\nScore: {}'.format(super().__str__(), self.__edited, self.__score)


class ArxivDocument(Document):
    """
    co_authors - list of co-authors
    """

    def __init__(self, entry: OrderedDict):
        author = entry['author']
        if type(author) is list:
            self.__co_authors = [co_author['name'] for co_author in author[1:]]
            author = author[0]
        else:
            self.__co_authors = []
        date = parse_arxiv_date(entry['published'])
        super().__init__(entry['title'], author['name'], date, entry['id'], entry['summary'])

    def get_co_authors(self):
        return self.__co_authors

    def set_co_authors(self, co_authors):
        self.__co_authors = co_authors

    def add_co_author(self, co_author):
        self.__co_authors.append(co_author)

    def remove_co_author(self, co_author):
        self.__co_authors.remove(co_author)

    def get_type(self):
        return 'Arxiv'

    def __str__(self):
        return '{}\nCo-authors: {}'.format(super().__str__(), ', '.join(self.__co_authors))
