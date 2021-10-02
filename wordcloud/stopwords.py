# Reads in stop words line by line from specified file
def set_stopwords(data_file):
    stopwords = {}
    with open(data_file) as file:
        for line in file:
            word = line.strip()
            if not word in stopwords:
                stopwords[word] = 1
    return stopwords