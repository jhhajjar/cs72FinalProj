from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import pandas as pd
import string
import os
import operator

# Reads the large dictionary
def readNRC(filename):
    wordToEmotions = dict()
    with open(filename, 'r') as fp:
        # Loop through lines
        for line in fp:
            line = line.strip('\n')
            # If no emotional value, skip
            if line[-1:] == '0':
                continue
            # Else analyze
            else:
                words = line.split('\t')
                if len(words) != 3:
                    continue
                word = words[0]
                emotion = words[1]
                # Store the emotions associated with the word
                if word not in wordToEmotions.keys():
                    wordToEmotions[word] = [emotion]
                else:
                    wordToEmotions[word].append(emotion)
    return wordToEmotions


def getWords(filename):
    """ Gets all of the words from a file.
    """
    # Get text from the file
    with open(filename, 'r') as fp:
        text = fp.read()

    punctuation = [ c for c in string.punctuation ] + [u'\u201c',u'\u201d',u'\u2018',u'\u2019']

    # Get words from the file
    words = []
    for word in word_tokenize(text):
        # Omit punctuation or digits
        if word in punctuation or word in string.digits:
            continue
        words.append(word)

    return words


def getEmotions(words, wordToEmotions):
    """ Gets all of the emotions from a list of words.
    """
    # Define the emotions
    emotions = {
        'anger': 0.0,
        'anticipation': 0.0,
        'disgust': 0.0,
        'fear': 0.0,
        'joy': 0.0,
        'negative': 0.0,
        'positive': 0.0,
        'sadness': 0.0,
        'surprise': 0.0,
        'trust': 0.0
    }

    # loop through the words and count the emotions
    for word in words:
        # if the word is in the dictionary
        if word in wordToEmotions.keys():
            # for each emotion associated with that word
            for emotion in wordToEmotions[word]:
                emotions[emotion] += 1

    # percentify
    total = sum(emotions.values())
    for key in emotions.keys():
        emotions[key] = emotions[key] / total * 100

    return emotions


def analyze(filename, wordToEmotions):
    """ Performs general analysis on the file
    """
    # Get all words from the file
    words = getWords(filename)
    # Get the emotions
    emotions = getEmotions(words, wordToEmotions)    

    return emotions


def main():
    # Create the word to emotion dictionary
    wordToEmotions = readNRC('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    dir = './sotu_speeches/'

    # Create data dictionary to hold all of the years emotions
    data = dict()

    # Loop through all files and analyze
    files = os.listdir(dir)
    for f in files:
        print(f'Analyzing {f[:4]}')
        data[f[:4]] = analyze(f'{dir}{f}', wordToEmotions)

    # Turn the data into a dataframe
    df = pd.DataFrame.from_dict(data, orient='index')

    # Make directory for graphs
    if not os.path.exists('graphs/'):
        os.makedirs('graphs/')

    # Plot each emotion
    for emotion in list(df):    
        fig = df[emotion].plot().get_figure()
        fig.savefig(f'graphs/{emotion}.png')
        fig.clf()


if __name__ == "__main__":
    main()
