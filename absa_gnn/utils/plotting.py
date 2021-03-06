from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import spacy
from nltk.tree import Tree
# from config import configuration as cfg


def tsne_plot(words, vectors):
    """
    Creates and TSNE model and plots it
    Args:
        words: list of words
        vectors: list of their correspoding vectors
    """

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(vectors)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i, x_value in enumerate(x):
        plt.scatter(x_value, y[i])
        plt.annotate(words[i],
                     xy=(x_value, y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


def visulaize_dependancy_tree(doc):
    from pathlib import Path
    svg = spacy.displacy.render(doc, style='dep', jupyter=False)
    output_path = Path('output/dependancy_tree.svg')
    output_path.open("w", encoding="utf-8").write(svg)


def nltk_spacy_tree(sent):
    """
    Visualize the SpaCy dependency tree with nltk.tree
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sent)

    def token_format(token):
        return "_".join([token.orth_, token.tag_, token.dep_])

    def to_nltk_tree(node):
        if node.n_lefts + node.n_rights > 0:
            return Tree(token_format(node), [to_nltk_tree(child)
                                             for child in node.children])
        else:
            return token_format(node)

    tree = [to_nltk_tree(sent.root) for sent in doc.sents]
    # The first item in the list is the full tree
    tree[0].draw()


if __name__ == "__main__":

    doc = "super fast processor and really nice graphics card. and plenty of storage with 250 gb(though I will upgrade this and the ram.)"
    nltk_spacy_tree(doc)
