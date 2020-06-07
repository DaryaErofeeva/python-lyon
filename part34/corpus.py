import itertools
import pickle
import re

from pandas import DataFrame, Series

from part1.script import join_docs


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
        self.__characters_chain = None

    def print(self, limit=5):
        sorted_docs = sorted(self.collection.values(), key=lambda doc: (doc.get_date(), doc.get_title()))[:limit]
        print(*sorted_docs)

    def __repr__(self):
        return {'name': self.name, 'author': list(self.id2aut.values()), 'docs': list(self.id2doc.values())}

    def save(self):
        with open('data.pickle', 'wb') as f:
            pickle.dump(self, f)

    def search(self, query, context_length=5):
        """
        4.1
        :param query: search keyword
        :param context_length: length left and right contexts that are returned
        :return: list of found extracts which contain keyword
        """
        if not self.__characters_chain:
            docs = [doc.formatted_doc() for doc in self.collection.values()]
            self.__characters_chain = join_docs(docs)
        re_context_length = '.{0,' + str(context_length) + '}'
        re_left_context = rf'{re_context_length}\b'
        re_right_context = rf'\b{re_context_length}'
        return re.findall(rf'{re_left_context}{query}{re_right_context}', self.__characters_chain)

    def concorde(self, query, context_length):
        """
        4.2
        :param query: search keyword
        :param context_length: length left and right contexts that are returned
        :return: pandas table with following columns [contexte gauche, motif trouvé, contexte droit]
        """
        return DataFrame(data=[result.partition(query) for result in self.search(query, context_length)],
                         columns=['contexte gauche', 'motif trouvé', 'contexte droit'])

    def stats(self, n):
        """
        4.4, 4.5, 4.6, 4.7
        :param n: amount of top frequent words to print
        """
        vocabulaire = {}
        words = []
        for key, value in self.collection.items():
            value_words = value.formatted_doc().split(' ')
            vocabulaire[key] = set(value_words)
            words += value_words

        print('\n========================= 4.5 =========================')
        print(vocabulaire)

        print('\n========================= 4.6 =========================')
        freq = Series(words).value_counts().rename_axis('word').to_frame('term frequency')
        print(freq)

        print('\n========================= 4.7 =========================')
        vocabulaire_words = list(itertools.chain.from_iterable(vocabulaire.values()))
        doc_freq = Series(vocabulaire_words).value_counts().rename_axis('word').to_frame('document frequency')
        print(freq.join(doc_freq))

        print('Le nombre de mots différents dans le corpus: {}'.format(len(freq)))
        print('Les {} mots les plus fréquents: {}'.format(n, freq.axes[0].tolist()[:n]))
