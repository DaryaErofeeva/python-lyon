import pickle


class Corpus:
    """
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
        sorted_docs = sorted(self.collection.values(), key=lambda doc: (doc.date, doc.title))[:limit]
        print(*sorted_docs)

    def __repr__(self):
        return {'name': self.name, 'author': list(self.id2aut.values()), 'docs': list(self.id2doc.values())}

    def save(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self, f)
