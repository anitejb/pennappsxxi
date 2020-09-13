import re

from gensim.models.ldamodel import LdaModel
from gensim.models import LdaMulticore
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from gensim.utils import simple_preprocess, lemmatize

import nltk
# nltk.download("averaged_perceptron_tagger")
# nltk.download("stopwords")
# nltk.download("wordnet")
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

#stop_words
stop_words = stopwords.words("english")
stop_words += ["word", "list", "let", "put"]

# Preprocess

# Create gensim dictionary form a single text file
# with open("src/nlp/psychTranscript1.txt", encoding="utf-8") as f:
#     file_lines = []
#     for line in f:
#         file_lines.append(simple_preprocess(line, deacc=True))
# dictionary = corpora.Dictionary(file_lines)
# print(file_lines)

# def preprocessWord(input):
#lemmatize
# data_processed=[]

class LDA:
    def __init__(self):
        self.all_phrases = []

    def get_wordnet_pos(self, word):
        """Map Part of Speech tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV
        }

        return tag_dict.get(tag, wordnet.NOUN)


    def preprocessing(self, sentence):
        doc_out=[]
        simple_preprocess_sentence = simple_preprocess(sentence)
        for wd in simple_preprocess_sentence:
            if wd not in stop_words:  # remove stopwords
                lmtzr = WordNetLemmatizer()
                lemmatized_word = lmtzr.lemmatize(wd, self.get_wordnet_pos(wd))
                if lemmatized_word:
                    doc_out.append(lemmatized_word)
            else:
                continue
        return [doc_out]


    # Feed to model
    def load_model(self, phrase):
        processed_phrase = self.preprocessing(phrase)

        self.all_phrases += processed_phrase

        dct = Dictionary(self.all_phrases)
        corpus = [dct.doc2bow(line) for line in self.all_phrases]

        lda_model = LdaMulticore(corpus=corpus,
                                id2word=dct,
                                random_state=100,
                                num_topics=10,
                                passes=10,
                                chunksize=1000,
                                batch=False,
                                alpha="asymmetric",
                                decay=0.5,
                                offset=64,
                                eta=None,
                                eval_every=0,
                                iterations=100,
                                gamma_threshold=0.001,
                                per_word_topics=True)

        topic_keywords = []
        topics = lda_model.print_topics(-1)
        # print(topics)
        for topic in topics[:5]:
            topics_str = topic[1]
            pattern = r"[^a-zA-Z+]"
            topics_list = re.sub(pattern, "", topics_str).split("+")
            topic_keywords += topics_list[:5]

        return topic_keywords

# Testing
if __name__ == "__main__":
    lda = LDA()
    phrase1 = "Today we're going to talk about memory. It is the study of the the brain."
    topic_keywords = lda.load_model(phrase1)
    print(topic_keywords)
    phrase2 = '''In the last section, we examined some early aspects of memory. In this section, what we’re going to do is discuss some factors that influence memory. So let’s do that by beginning with the concept on slide two, and that concept is overlearning. Basically in overlearning, the idea is that you continue to study something after you can recall it perfectly. So you study some particular topic whatever that topic is. When you can recall it perfectly, you continue to study it.
This is a classic way to help when one is taking comprehensive finals later in the semester. So when you study for exam one and after you really know it all, you continue to study it. That'''
    topic_keywords = lda.load_model(phrase2)
    print(topic_keywords)

# [
#     (0, "0.034*"recall" + 0.022*"learn" + 0.016*"slide" + 0.014*"well" + 0.012*"one" + 0.011*"take" + 0.011*"first" + 0.011*"call" + 0.011*"try" + 0.010*"show""),
#      (1, "0.009*"exam" + 0.007*"help" + 0.007*"take" + 0.007*"study" + 0.006*"many" + 0.006*"coca" + 0.006*"cola" + 0.006*"variety" + 0.005*"comprehensive" + 0.005*"way"")
# ]


# Update & Loop

# common_dictionary = Dictionary(common_texts)
# common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]

# print(common_dictionary)
# print(common_corpus)

# word_counts = [[(common_dictionary[id], count) for id, count in line] for line in common_corpus]
# print(word_counts)



# topics = lda.print_topics(num_words=4)
# for topic in topics:
#     print(topic)

# other_texts = [
#     ["computer", "time", "graph"],
#     ["survey", "response", "eps"],
#     ["human", "system", "computer"]
# ]
# other_corpus = [common_dictionary.doc2bow(text) for text in other_texts]

# unseen_doc = other_corpus[0]
# vector = lda[unseen_doc]

# lda.update(other_corpus)
# vector = lda[unseen_doc]

# topics = lda.print_topics(num_words=4)
# for topic in topics:
#     print(topic)
