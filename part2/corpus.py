import pickle


class Corpus:
    """
    2.7
    name - name
    author - dictionary of instances of class Author
    id2aut - dictionary of authors' indexes
    collection - dictionary of instances of class Document
    id2doc -  dictionary of documents' indexes
    ndoc - documents count
    nauth - authors count
    """

    def __init__(self, name, author, id2aut, collection, id2doc, ndoc, nauth):
        self.name = name
        self.author = author
        self.id2aut = id2aut
        self.collection = collection
        self.id2doc = id2doc
        self.ndoc = ndoc
        self.nauth = nauth

    def print(self, limit=5):
        """
        2.8
        Sorts documents by date and title
        :param limit: amount of docs to return
        :return: list of sorted docs of length 'limit'
        """
        sorted_docs = sorted(self.collection.values(), key=lambda doc: (doc.date, doc.title))[:limit]
        print(*sorted_docs)

    def __repr__(self):
        """
        2.8
        :return: collection that presents corpus
        """
        return {'name': self.name, 'author': list(self.id2aut.values()), 'docs': list(self.id2doc.values())}

    def save(self, filename):
        """
        2.9
        :param filename: filename where corpus should be saved
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
