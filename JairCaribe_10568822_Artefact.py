# -*- coding: utf-8 -*-
"""Trump_v6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1T89mwosGPbIHUMkbcCRiMh_LQVDK-xbV

# Install 
installing such libraries

To extract sentiments from Donald Trump's tweets it is necessary to use the Lexico-based sentiment analysis tool called VADER which was introduced in 2014 to deal with social media texts (I. Awajan et al. 2021) this model uses the combination of lexicals able to label sentences as positive, negative, or neutral. This technique is quite popular as it works very well with social media texts, no training data is needed as it is built from a generalized feeling lexicon, fast enough to be used online with uncompensated streaming data between speed and performance, it detects feelings of slang, in addition to being an open source, (E. Saad et al, 2021) several authors used VADER in the studies and found that this technique has the performance similar to that of human evaluators.
"""

#installing vaderSentiment
!pip install vaderSentiment

!pip install numpy pandas

"""# **Import**
Importing all the libraries That I need for my analysis
"""

import numpy as np
import pandas as pd # data processing, CSV file
import re # data preparation, cleaning data
import string

"""# **Getting the Data**"""

from google.colab import drive
drive.mount("/content/drive", force_remount=True)

# Importing dataset and examining it

dataset = pd.read_csv("/content/drive/My Drive/bd/tweets_01-08-2021.csv", encoding="latin-1")

"""# **Understanding the database**

---


"""

# Checking rows and columns
print(dataset.head())

#Checking details of the dataset
print(dataset.info())

dataset.describe(include="all").T

"""CHECKING DUPLICATED IDS"""

print('Value Counts: {}'.format(dataset['id'].value_counts().sum()))
print('Number of Entries: {}'.format(dataset.shape[0]))

#checking missing value
dataset.isnull().sum()

print (dataset.describe())

dataset.head()

#Checking if there is repeated ID, if there is I should delete
dataset['id'].value_counts()

#checking the dataset shape
print(dataset.shape)

#Using only the column that I need
data = dataset[["text","favorites","retweets","date"]]

data.head

"""# **DATA PREPARATION**
??? Make all text lowercase;

??? Remove links;

??? Remove tags;

??? Remove breaklines;

??? Remove words with numbers inside;

??? Remove punctuations;

??? Remove accents;

??? Remove duplicated whitespaces
"""

import unicodedata

#Filter to remove links
data['text'].iloc[1000]

re.sub('https?://\S+|www\.\S+', '', data['text'].iloc[1000])

#Filter to remove tags
re.sub('<.*?>+', ' ', '<h1>TEXT</h1>')

re.sub('\[.*?\]', '', '[tag]TEXT[--tag]')

#Filter to remove words with numbers inside
re.sub('\w*\d\w*', ' ', 'sea3sky blue today')

#Filter to remove duplicate whitespaces
re.sub(r'\s+', ' ', 'A B C              D')

#Filter to remove punctuation
data['text'].iloc[60]

re.sub(r'[^\w\s]', '', data['text'].iloc[60])

#Filter to remove accents
data['text'].iloc[1002]

text = data['text'].iloc[1002]
text = unicodedata.normalize('NFKD', text)
text = "".join([c for c in text if not unicodedata.combining(c)])
print(text)

#checking how the tweets are know, If it is clean or not
data['text']

# Checking the tweets from 100 to 115 using ILOC to select the rows
data['text'].iloc[100:115]

"""# **Vader Sentiment **


"""

# Using VaderSentiment to define tweet's score, know what should be positive, negative and neutral. 
#Used polarity_scores() method to get the sentiment metrics for a piece of text.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyser = SentimentIntensityAnalyzer()
scores=[]
for i in range(len(data['text'])):
    
    score = analyser.polarity_scores(data['text'][i])
    score=score['compound']
    scores.append(score)
sentiment=[]
for i in scores:
    if i>=0.05:
        sentiment.append('Positive')
    elif i<=(-0.05):
        sentiment.append('Negative')
    else:
        sentiment.append('Neutral')
data['sentiment']=pd.Series(np.array(sentiment))

#Checking which tweets are positive negative and neutral
data.head()

#Grouping sentiment as POSITIVE, NEGATIVE AND NEUTRAL and counting how many tweets there are per group
temp = data.groupby('sentiment').count()['text'].reset_index().sort_values(by='text',ascending=False)
temp.style.background_gradient(cmap='Purples')

#Plotly is a Python library that is used to generate graphs, rather than that it allows us to view these graphs interactively.
!pip install plotly

#Python Matplotlib is a Python programming language library used for data visualization and graphical plotting.
!pip install matplotlib seaborn

"""## **Number of favorites and retweets by year**"""

import matplotlib.pyplot as plt

data["date"] = pd.to_datetime(data["date"]) 
data["date"].apply(lambda x: x.year) # getting all years 

# Number of tweets by year
colors = []
for i in range(2020-2009+1):
    x = 0.7-0.06*i
    c = (x,x,0.5)
    colors.append(c)
    
# Creating the visualization
fig = plt.figure(figsize = (10,4))
ax = fig.add_axes([0,0,1,1])
ax.set_title("Quantity of favorites, retweets of Trump's tweets", fontsize=20)
ax.tick_params(labelsize=10)

# Number of tweets (more details)
data["year_month"] = data["date"].apply(lambda x: str(x.year)+"-"+str(x.month))
data["year_month"] = pd.to_datetime(data["year_month"])
year_month = pd.pivot_table(data, values = "text", index = "year_month", aggfunc = "count")

# Average number of "favorites"
year_month = pd.pivot_table(data, values = "favorites", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 3)

# Average number of "retweets"
year_month = pd.pivot_table(data, values = "retweets", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 3)


ax.legend(["Favorites","Retweets"], fontsize=15)
ax.tick_params(labelsize=18)
plt.show()

"""### **Mean positivity/negativity/neutrality of Trump's tweets by year**"""

# Calculate the polarity of the tweets of Trump with NLTK
#giving a polarity to the text positives, negative and neutral using the function  .APPLY 
#because it has good performance when to the same tinha many times
#Then I created a vizualization aggfunc function to give the mean to the sentiment
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

data["polarity"] = data["text"].apply(lambda x: analyser.polarity_scores(x))

data["pos"] = data["polarity"].apply(lambda x: x["pos"])
data["neg"] = data["polarity"].apply(lambda x: x["neg"])
data["neu"] = data["polarity"].apply(lambda x: x["neu"])
data["compound"] = data["polarity"].apply(lambda x: x["compound"])

# Creating a visualization
ax.set_title("Mean positivity/negativity/neutrality of Trump's tweets by year", fontsize=20)
fig = plt.figure(figsize = (10,8))#size of image
ax = fig.add_axes([0,0,1,1])
ax.tick_params(labelsize=10)

# Positive plot
year_month = pd.pivot_table(data, values = "pos", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 5)

# Negative plot
year_month = pd.pivot_table(data, values = "neg", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 5, color = "red")

# Neutral plot
year_month = pd.pivot_table(data, values = "neu", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 5, color = "green")


ax.legend(["pos","neg","neu"], fontsize=15)
ax.tick_params(labelsize=15)

plt.show()

"""# Positivity/negativity/neutrality composites of Trump's tweets by year"""

# Create the visualization
fig = plt.figure(figsize = (10,6))
ax = fig.add_axes([0,0,1,1])
ax.set_title("Mean positivity/negativity/neutrality of Trump's tweets by year", fontsize=24)
ax.tick_params(labelsize=14)

# Compound plot
data["year_month"] = data["date"].apply(lambda x: str(x.year)+"-"+str(x.month))
data["year_month"] = pd.to_datetime(data["year_month"])
year_month = pd.pivot_table(data, values = "compound", index = "year_month", aggfunc = "mean")
ax.plot(year_month, lw = 5, color = "blue")


ax.legend(["pos","neg","neu"], fontsize=18)

plt.legend("")
plt.show()

"""# **Correlation between retweets, favorites and positivity**"""

# to know if his positives tweets influence the quantity of retweets/favorites need to 
#Look at the number of favorites and retweets is the way to know if people are interested in what Donald Trump tweeted.
#to do this I used a graph to show the correlation between retweets, favorites and compound. There is a high correlation 
#between favorites and retweets and low correlation between compound and retweets and favorites
#used function as annot to show the value inside the graph 
#used cmap for colour

import seaborn as sns
plt.figure(figsize = (9,5))
plt.title("Correlation between retweets, favorites and positivity\n", fontsize = 10)
sns.heatmap(data[[ "pos","retweets","favorites"]].corr(), annot = True, cmap="BuPu")
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')
plt.figure(figsize=(12,6))
import plotly.graph_objs as go
sns.countplot(x='sentiment',data=data)

fig = go.Figure(go.Funnelarea(
    text =temp.sentiment,
    values = temp.text,
    title = {"position": "top center", "text": "Funnel-Chart of Sentiment Distribution"}
    ))
fig.show()

"""## Install WordCloud"""

#library used to display a word cloud
!pip install WordCloud

"""## Words to ignore"""

#ignoring the words I don't want to show
to_ignore = ['realdonaldtrump', 'rt']

"""## WordCloud"""

from wordcloud import WordCloud, STOPWORDS , ImageColorGenerator
import re

tweet_All = " ".join(re.sub(r"\b[a-zA-Z]\b", "", review) for review in data.text)
for ig in to_ignore:
    tweet_All = tweet_All.replace(ig, '')


fig, ax = plt.subplots(1, 1, figsize  = (10,10))
# Create and generate a word cloud image:
wordcloud_ALL = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(tweet_All)

# Display the generated image:
ax.imshow(wordcloud_ALL, interpolation='bilinear')

ax.axis('off')

#printing tweets and sentiments
data.head(n=10)

"""# Histogram of Positive, Negative and Neutral Adjectives"""

!pip install nltk # installing the NLTK is a leading platform for building Python programs to work with human language data.
import nltk
nltk.download('punkt') #This tokenizer divides a text into a list of sentences
nltk.download('averaged_perceptron_tagger')#is used for tagging words with their parts of speech (POS). We also need to set the add this directory to the NLTK data path.
nltk.download('wordnet')#used for the lemmatization

from nltk.stem import PorterStemmer # library to Stemming words
from nltk.tokenize import word_tokenize # library to tokenizing words

"""## List with all words and remove duplicates"""

# creating a list of words using the method word_tokenize() to split a sentence into words,
# removing duplicates tweets ( if word not in tweet_words: ) if there is the word will not add again
#then use the method append to create a list for words and show how many hows we have.
tweet_words = []
for word in word_tokenize(tweet_All):
    if word not in tweet_words:
        tweet_words.append(word)
print('Number of words: {}'.format(len(tweet_words)))

#Showing from 0 to 10 tweets 
tweet_words[0:10]

"""## Tokenize and separate the adjectives"""

# separating a piece of text into smaller, separating the adjectives, 
#using pos_tag takes each list of the word, 
#compares it with the database, to know if it is an adjective, verb
#each element of the list becomes a tuple and when is JJ it is adjective
#searches the list for just the word that is JJ and and adds adjective list
#then print the amount of adjectives

words_tags = nltk.pos_tag(tweet_words)
tweet_adj = []
for word_tag in words_tags:
    if word_tag[1] == 'JJ':
        tweet_adj.append(word_tag[0])
        
print('Number of adjectives: {}'.format(len(tweet_adj)))
words_tags

"""### ADJETIVOS TOKENIZADOS"""

nltk.download('words')
nltk.download('universal_tagset')

#Check if a word is an adjective based on nltk.word_tokenize
possible_adjectives = []
for word in tweet_adj:
    cat = nltk.word_tokenize(word)
    if nltk.pos_tag(cat, tagset='universal')[0][1] == 'ADJ': possible_adjectives.append(word)

# Filters words using nltk.corpus.words dictionary
wordset = nltk.corpus.words.words()
filter_w = lambda word: word in wordset
filtered_words = list(filter(filter_w, possible_adjectives))

count = 0
for word in filtered_words:
    print(word, end=', ')
    count += 1
    if (count % 10 == 0): print("")

"""## Stemming

Do not need to do stemming. Do Lemmatization
"""

#using the algorithm (???Porter stemmer???) to remove inflexional endings from words.
#just take the root of the words
ps = PorterStemmer()
tweet_adj_stemmed = []
for word in tweet_adj:
    sword = ps.stem(word)
    if sword in tweet_adj_stemmed:
        sword += '_duplicated'
    tweet_adj_stemmed.append(sword)

#Showing from 1 to 10 tweets 
tweet_adj_stemmed[1:50]

"""## Lemmatization"""

from nltk.stem import WordNetLemmatizer

# get the meaning of the word
lmt = WordNetLemmatizer()
filtered_words_lemmatized = []
for word in filtered_words:
    lword = lmt.lemmatize(word)
    if lword in filtered_words_lemmatized:
        lword += '_duplicated'
    filtered_words_lemmatized.append(lword)

filtered_words_lemmatized[1:50]

"""## Choose Stemming or Lemmatization"""

#tweet_adj_pos = tweet_adj_stemmed
tweet_adj_pos = filtered_words_lemmatized

"""## DataFrame with positive, neutral and negative counters for the adjectives"""

#to count the word to see how many there are positive, negative, and neutral
#get the variable global data
#for each row in the column , this will check if the word is there
#check if the row is positive, negative or neutral
#add which sentiment it fits
def count_pnn(word):
    global data
    
    positive = 0
    negative = 0
    neutral = 0
    for i in range(data.shape[0]):
        if word in data['text'].iloc[i]:
            if data['sentiment'].iloc[i] == 'Positive':
                positive += 1
            elif data['sentiment'].iloc[i] == 'Negative':
                negative += 1
            elif data['sentiment'].iloc[i] == 'Neutral':
                neutral += 1
                
    return (positive, negative, neutral)

len(filtered_words)

"""## ! **Long processing time**: Avoid this by loagind the adj DataFrame from csv!"""

#for each word in the list, it will be used to make another list that will be the positive, negative and neutral count.
#pnn returns the tuple, then joins the word with the one that came back from the tuple and adds it to the list
data_adj = []
for i in range(len(filtered_words)):
    if '_duplicated' in tweet_adj_pos[i]:
        for j in range(len(data_adj)):
            if data_adj[j][0] == tweet_adj_pos[i][:-11]:
                pos, neg, neu = count_pnn(filtered_words[i])
                data_adj[j][1] += pos
                data_adj[j][2] += neg
                data_adj[j][3] += neu
    else:
        pos, neg, neu = count_pnn(filtered_words[i]) # Counting with the orginal word
        data_adj.append([tweet_adj_pos[i], pos, neg, neu]) # Add the stemmed or lemmatized word and counters
#creating a dataframe with the columns names
adj = pd.DataFrame(data_adj, columns =['Word', 'Positive', 'Negative', 'Neutral'])

adj

"""## Save adj DataFrame in csv and serialized object (do not overwrite previously saved)"""

# to save
#if you have not saved saves to disk
# .pkl it is the file type the binary of the object
# .csv most used and most compatible file
import os

if not os.path.isfile('trump_twitter_adjectives.pkl'):
    adj.to_pickle('trump_twitter_adjectives.pkl')
if not os.path.isfile('trump_twitter_adjectives.csv'):
    adj.to_csv('trump_twitter_adjectives.csv', index = False)

"""## Load adj DataFrame from csv"""

adj = pd.read_csv('trump_twitter_adjectives.csv')

"""## Analisis of Adjectives"""

#checking the 15 firsts adjectives
adj.head(n=15)

"""### Positive adjectives most frequent"""

adj.sort_values(by=['Positive'], ascending=False).head(n=50)

adj.sort_values(by=['Positive'], ascending=False).iloc[100:150]

new_cols = adj.columns.copy()
new_cols = new_cols.to_list()
new_cols.remove('Positive')
new_cols.remove('Word')
adj_pos_10 = adj.sort_values(by=['Positive'], ascending=False).head(n=10).drop(columns=new_cols)
print(adj_pos_10)

labels = list(adj_pos_10['Word'])
ax = adj_pos_10.plot(kind='bar', figsize=(25, 13), title='Positive Frequency', legend=False, x='Word')
plt.ylabel('Frequency')

"""### Negative adjectives most frequent"""

new_cols = adj.columns.copy()
new_cols = new_cols.to_list()
new_cols.remove('Negative')
new_cols.remove('Word')
adj_pos_10 = adj.sort_values(by=['Negative'], ascending=False).head(n=10).drop(columns=new_cols)
print(adj_pos_10)

labels = list(adj_pos_10['Word'])
ax = adj_pos_10.plot(kind='bar', figsize=(25, 13), title='Negative Frequency', legend=False, x='Word')
plt.ylabel('Frequency')

"""### Neutral adjectives most frequent"""

new_cols = adj.columns.copy()
new_cols = new_cols.to_list()
new_cols.remove('Neutral')
new_cols.remove('Word')
adj_pos_10 = adj.sort_values(by=['Neutral'], ascending=False).head(n=10).drop(columns=new_cols)
print(adj_pos_10)


labels = list(adj_pos_10['Word'])
ax = adj_pos_10.plot(kind='bar', figsize=(25, 13), title='Neutral Frequency', legend=False, x='Word')
plt.ylabel('Frequency')