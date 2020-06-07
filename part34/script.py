import re

from part2.script import Author
from part34.corpus import Corpus
from part34.factory import DocumentsFactory


def nettoyer_texte(text):
    """
    4.4
    :param text: string to clean
    :return: only alpha symbols from input text in lower case
    """
    return re.sub(r'[^a-zA-Z]+', ' ', text)


if __name__ == "__main__":
    docs = DocumentsFactory().create_documents()
    collection = {}  # alternative way {i: docs[i] for i in range(len(docs))}
    authors = {}
    for index in range(len(docs)):
        collection[index] = docs[index]
        author = Author(docs[index].get_author())
        try:
            author_index = list(authors.values()).index(author)
            authors[author_index].add(docs[index])
        except ValueError:
            author.add(docs[index])
            authors[len(authors)] = author

    id2doc = {key: value.get_title() for key, value in collection.items()}
    print(id2doc)

    id2aut = {key: value.name for key, value in authors.items()}
    print(id2aut)

    corpus = Corpus('Corpus', authors, id2aut, collection, id2doc, len(collection), len(authors))
    corpus.print()

    print('\n========================= 4.1 =========================')
    print(corpus.search('Minecraft'))

    print('\n========================= 4.2 =========================')
    print(corpus.concorde('Minecraft', 7))

    print('\n========================= 4.3 =========================')
    print(corpus.collection[0].get_summarization())

    print('\n========================= 4.4 =========================')
    print(nettoyer_texte('Minecraft 2.0 hello, duuude'))

    corpus.stats(6)
