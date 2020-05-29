from part2.script import Author
from part3.corpus import Corpus
from part3.factory import DocumentsFactory

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
