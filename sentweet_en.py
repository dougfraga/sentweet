"""
https://www.youtube.com/watch?v=ujId4ipkBio
https://www.youtube.com/watch?v=pgZcP852dMg
"""

# Import the libraries
import tweepy
from textblob import TextBlob
from googletrans import Translator
import pandas as pd
import numpy as np
import re

keywords = 'frouxonaro'


# Functions
def getSubjectivity(text):
    """Create a function to get the subjectivity"""
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    """Create a function to get the polarity"""
    return TextBlob(text).sentiment.polarity


def getAnalysis(score):
    """Compute the negative, neutral and positive analysis"""
    if score < 0:
      result = 'Negative'
    elif score == 0:
      result = 'Neutral'
    else:
      result = 'Positive'

    return result


# Import DataFrame
df = pd.read_csv(f'tweets_{keywords}.txt', sep='\t', encoding='utf-8')


# Translate content
lines = []
for line in df['Tweet']:
    trans = Translator()
    trans_text = trans.translate(line, src="pt", dest="en")
    lines.append(trans_text.text)
df['English'] = lines


# Create two new columns for subjectivity and polarity
df['Subjectivity'] = df['English'].apply(getSubjectivity)
df['Polarity'] = df['English'].apply(getPolarity)


# Compute the negative, neutral and positive analysis
df['Analysis'] = df['Polarity'].apply(getAnalysis)

pd.options.display.width = 1000
print(df['Tweet'].values)

df.to_csv(f'tweets_{keywords}_en.txt', sep='\t', encoding='utf-8', index=False)

# Plot the polarity and subjectivity
#plt.figure(figsize=(8,6))
#for i in range(0,df.shape[0]):
#  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')
#
#plt.title('Sentiment Analysis')
#plt.xlabel('Polarity')
#plt.ylabel('Subjectivity')

