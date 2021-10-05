import itertools

# Creates vocabularity of num_words given data_file and a list of stopwords (words to exclude)
def create_vocab(num_words, data_file, stopwords):
    vocab = {}
    with open(data_file) as file:
        for line in file:
            sentence = line.strip().replace('.', '').replace(',', '').replace('!', '').replace('?', '').replace(':', '').replace(';', '').replace('--',' ').replace('"', '').replace('(','').replace(')','').replace('\'s', '').replace('\'', '').lower()

            words = sentence.split()
            for word in words:
                if word in stopwords:
                    pass
                elif not word in vocab:
                    vocab[word] = 1
                else:
                    vocab[word] += 1

    sorted_words = {k: v for k, v in sorted(vocab.items(), key=lambda item: item[1])}
    if len(sorted_words) > num_words:
        sorted_words = dict(itertools.islice(sorted_words.items(), len(sorted_words)-num_words, None))
    print("%d most common words; %s" % (num_words, sorted_words))
    return sorted_words