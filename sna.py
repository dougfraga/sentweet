import tweepy
import pandas as pd
import networkx as nx
from community import community_louvain
import matplotlib.pyplot as plt


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


api = tweet_con('Login.txt')

df = pd.read_csv('networkOfFollowers.csv') #Read into a df
G = nx.from_pandas_edgelist(df, 'source', 'target')
nodes = G.number_of_nodes() #Find the total number of nodes in this graph

G_sorted = pd.DataFrame(sorted(G.degree, key=lambda x: x[1], reverse=True))
G_sorted.columns = ['names','degree']

u = api.get_user(user_id = int(G_sorted['names'].iloc[0]))

G_tmp = nx.k_core(G, 8) #Exclude nodes with degree less than 2

partition = community_louvain.best_partition(G_tmp)
#Turn partition into dataframe
partition1 = pd.DataFrame([partition]).T
partition1 = partition1.reset_index()
partition1.columns = ['names','Label']

combined = pd.merge(G_sorted, partition1, how='left', left_on="names",right_on="names")

combined = combined.rename(columns={"names": "ID"}) #I've found Gephi really likes when your node column is called 'Id'
edges = nx.to_pandas_edgelist(G_tmp)
nodes = combined['ID']
edges.to_csv("edges.csv", index=False)
combined.to_csv("nodes.csv", index=False)

#pos = nx.spring_layout(G)
#f, ax = plt.subplots(figsize=(10, 10))
#plt.style.use('ggplot')
##cc = nx.betweenness_centrality(G2)
#nodes = nx.draw_networkx_nodes(G, pos,
#                               cmap=plt.cm.Set1,
#                               node_color=combined['group'],
#                               alpha=0.8)
#nodes.set_edgecolor('k')
#nx.draw_networkx_labels(G, pos, font_size=8)
#nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.2)
#plt.savefig('twitterFollowers.png')

