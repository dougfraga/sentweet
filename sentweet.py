"""
https://www.youtube.com/watch?v=ujId4ipkBio
https://www.youtube.com/watch?v=pgZcP852dMg
"""

# Import the libraries
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import networkx as nx
plt.style.use('fivethirtyeight')


# Functions
def tweet_con(credentials_file):
    """Connect and authenticate Twitter API"""
    
    log = pd.read_csv(credentials_file)

    consumerKey = log['key'][0]
    consumerSecret = log['key'][1]
    bearerToken = log['key'][2]
    accessToken = log['key'][3]
    accessTokenSecret = log['key'][4]

    # Create the authentication object
    authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

    # Set the access token and access token secret
    authenticate.set_access_token(accessToken, accessTokenSecret)

    # Create the API object while passing in tne auth information
    api = tweepy.API(authenticate, wait_on_rate_limit = True)

    return api


def cleanTxt(text):
    """Filter undesirable characters"""
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https?:\/\/\S+', '', text)
    text = re.sub(r':', '', text)

    return text


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


# Connect to Twitter API
api = tweet_con('Login.txt')


# Extract information
me = api.get_user(screen_name = '77_frota')

user_list = [me.id]
follower_list = []
for user in user_list:
    followers = []
    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=user).pages():
            followers.extend(page)
            print(len(followers))
    except tweepy.errors:
        print("error")
        continue
    follower_list.append(followers)

df = pd.DataFrame(columns=['source','target']) #Empty DataFrame
df['target'] = follower_list[0] #Set the list of followers as the target column
df['source'] = me.id #Set my user ID as the source


user_list = list(df['target']) #Use the list of followers we extracted in the code above
for userID in user_list:
    print(userID)
    followers = []
    follower_list = []

    # fetching the user
    user = api.get_user(user_id = userID)

    # fetching the followers_count
    followers_count = user.followers_count

    try:
        for page in tweepy.Cursor(api.get_follower_ids, user_id=userID).pages():
            followers.extend(page)
            print(len(followers))
            if followers_count >= 5000: #Only take first 5000 followers
                break
    except tweepy.errors:
        print("error")
        continue
    follower_list.append(followers)
    temp = pd.DataFrame(columns=['source', 'target'])
    temp['target'] = follower_list[0]
    temp['source'] = userID
    df = df.append(temp)
    df.to_csv("networkOfFollowers.csv")





G = nx.from_pandas_edgelist(df, 'source', 'target') #Turn df into graph
pos = nx.spring_layout(G) #specify layout for visual


f, ax = plt.subplots(figsize=(10, 10))
plt.style.use('ggplot')
nodes = nx.draw_networkx_nodes(G, pos,
                               alpha=0.8)
nodes.set_edgecolor('k')
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)
plt.show()



# Extract infos
#posts = tweepy.Cursor(api.search_tweets, q='douglas').items(10)
#posts = api.user_timeline(screen_name = "MarkRuffalo", count = 100, tweet_mode = "extended")
# Create a dataframe with a column called Tweets
#df = pd.DataFrame([tweet.text for tweet in posts], columns=['Tweets'] )


# Clean the text
#df['Tweets'] = df['Tweets'].apply(cleanTxt)


# Create two new columns for subjectivity and polarity
#df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
#df['Polarity'] = df['Tweets'].apply(getPolarity)


# Plot the Word Cloud
#allWords = ' '.join([twts for twts in df['Tweets']])
#wordCloud = WordCloud(width = 500, height = 300, random_state = 21, max_font_size = 119).generate(allWords)
#
#plt.imshow(wordCloud, interpolation = 'bilinear')
#plt.axis('off')
#plt.show()
#plt.close()


# Compute the negative, neutral and positive analysis
#df['Analysis'] = df['Polarity'].apply(getAnalysis)


# Plot the polarity and subjectivity
#plt.figure(figsize=(8,6))
#for i in range(0,df.shape[0]):
#  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='Blue')
#
#plt.title('Sentiment Analysis')
#plt.xlabel('Polarity')
#plt.ylabel('Subjectivity')

