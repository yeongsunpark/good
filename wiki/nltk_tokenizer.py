import time
from collections import Counter
from itertools import chain
from nltk.corpus import brown
from nltk import sent_tokenize, word_tokenize


start = time.time()
string_corpus = brown.raw() # Plaintext, str type.
tokenized_corpus = [word_tokenize(sent) for sent in sent_tokenize(string_corpus)]
fdist = Counter(chain(*tokenized_corpus))
end = time.time() - start


print(end)
