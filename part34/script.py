from part2.script import Author
from part34.corpus import Corpus, nettoyer_texte
from part34.factory import DocumentsFactory

if __name__ == "__main__":
    print('\n+++++++++++++++++++++++ PART 3 +++++++++++++++++++++++')

    print('=================== 3.1 | 3.4 | 3.5 ===================')
    print(DocumentsFactory.reddit_documents('University', 5)[0])

    print('\n=================== 3.2 | 3.4 | 3.5 ===================')
    print(DocumentsFactory.arxiv_documents('University', 5)[0])

    print('\n====================== 3.3 | 3.5 ======================')
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
    id2aut = {key: value.name for key, value in authors.items()}

    corpus = Corpus('Corpus', authors, id2aut, collection, id2doc, len(collection), len(authors))
    print(corpus)

    print('\n+++++++++++++++++++++++ PART 4 +++++++++++++++++++++++')

    print('========================= 4.1 =========================')
    print(corpus.search('Minecraft'))

    print('\n========================= 4.2 =========================')
    print(corpus.concorde('Minecraft', 7))

    print('\n========================= 4.3 =========================')
    print(corpus.collection[0].get_summarization())

    print('\n========================= 4.4 =========================')
    print(nettoyer_texte('Minecraft 2.0 hello, duuude'))

    corpus.stats(7)
