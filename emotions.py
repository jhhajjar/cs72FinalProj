from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import string
import os
import random


def readNRC(filename):
    """ Reads the NRC lexicon into a dictionary.
    """
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
    """ Performs general analysis on the file.
    """
    # Get all words from the file
    words = getWords(filename)
    # Get the emotions
    emotions = getEmotions(words, wordToEmotions)    

    return emotions


def readDates():
    """ Reads in the dates file into a list of lists.
    """
    dates = dict()
    with open('dates.txt', 'r') as fp:
        lines = fp.readlines()
    for line in lines:
        # This is the stupidest line ever but it splits the dates from the date
        # file into a list of list of all of the date ranges
        dates[line.split(':')[0]] = [list(range(int(x.split('-')[0]), int(x.split('-')[1])+1)) for x in line.strip('\n').split(':')[1].split(',')]
        
    return dates

def mkdir(dirname):
    """ Simple function to make a directory.
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)
            

# Generates all of the graphs
def graphDates(df, dates):
    """ Graphs the data in the dataframe with appropriate dates.
    """
    colors = {
        'wars': 'red',
        'pandemics': 'orange',
        'recessions': 'blue'
    }

    # Loop through each emotion and each event for each emotion
    for emotion in list(df):  
        for event in dates.keys():
            # Plot the graph
            df[emotion].plot()

            # Create the span in the graph
            for date in dates[event]:
                start = int(date[0])
                end = int(date[-1])
                plt.axvspan(start, end, alpha=0.20, color=colors[event])

            # Label and title the graph
            plt.xlabel('Year')
            plt.ylabel('Percentage of Words Conveying This Emotion')
            plt.title(f'{emotion.upper()} during {event.title()}')

            # Save and clear
            mkdir(event)
            plt.savefig(f'{event}/{emotion}_{event}.png')
            plt.clf()


def graphAverages(df):
    """ Graphs the averages of each emotion by event.
    """
    avgdir = 'averages/'
    mkdir(avgdir)
    for emotion in list(df):
        df[emotion].plot(kind='bar', rot=0, color=(random.random(),random.random(),random.random()))

        plt.xlabel('Events')
        plt.ylabel('Percentage of Words Conveying Emotion')
        plt.title(f'Average Percentage of {emotion.upper()} Words')

        plt.savefig(f'{avgdir}{emotion}.png')
        plt.clf()


def getMeans(df, dates):
    """ Generates the means for each emotion and each event type.
    """
    means = dict()
    for emotion in list(df):
        # Dictionary to store the mean for each emotion
        means[emotion] = dict()
        arr = df[emotion].values
        means[emotion]['average'] = round(np.nanmean(arr), 2)
        for event in dates.keys():

        # Get the mean of all values and for the event years
            means[emotion][event] = round(np.nanmean([arr[i-1900] for i in dates[event]]), 2)
            means[emotion][event] = round(np.nanmean([arr[i-1900] for i in dates[event]]), 2)
            means[emotion][event] = round(np.nanmean([arr[i-1900] for i in dates[event]]), 2)
    
    return pd.DataFrame.from_dict(means)


def main():
    # Create the word to emotion dictionary
    # wordToEmotions = readNRC('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    # dir = './sotu_speeches/'

    # # Create data dictionary to hold all of the years emotions
    # data = dict()

    # # Loop through all files and analyze
    # files = os.listdir(dir)
    # for f in files[:]:
    #     year = int(f[:4])
    #     print(f'Analyzing {year}')
    #     data[year] = analyze(f'{dir}{f}', wordToEmotions)

    # # Turn the data into a dataframe and add 1933
    # years_df = pd.DataFrame.from_dict(data, orient='index')
    # years_df = years_df.append(pd.Series([np.nan]*len(list(years_df)), index=[emotion for emotion in list(years_df)], name=1933))
    years_df = pd.read_csv('data.csv')

    # Read the dates for important events
    dates = readDates()

    # Graph each emotion
    # graphDates(years_df, dates)

    # Reformat the dates dictionary for taking means, turn from list of lists to list
    for event in dates.keys():
        dates[event] = [x for li in dates[event] for x in li]
        
    # Make a dataframe to compare the average emotion for each event
    means_df = getMeans(years_df, dates)
    # print(means_df)
    graphAverages(means_df)

if __name__ == "__main__":
    main()
