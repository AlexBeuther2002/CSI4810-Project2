from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt


sia = SentimentIntensityAnalyzer()
#========Creating the Year Graph========#
hot100df = pd.read_csv('Hot100_2010-2023.csv')
hot100df = hot100df[['Year', 'Song', 'Singer', 'Lyrics']]
hot100df = hot100df.dropna(subset=['Lyrics', 'Song', 'Singer'])

# Calculate sentiment for each song
hot100df['Sentiment'] = hot100df['Lyrics'].apply(lambda lyrics: sia.polarity_scores(lyrics)['compound'])

avgsentiment = hot100df.groupby(['Year'])['Sentiment'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

for year, group_df in avgsentiment.groupby('Year'):
    ax.bar(str(year), group_df['Sentiment'].values[0], label=str(year))

ax.set_xlabel('Year')
ax.set_ylabel('Average Sentiment')
plt.title("Sentiment Over the Years")
plt.xticks(rotation=45, ha='right')
plt.show()



#==============Creating the Singer Graph==========#
# Split singers apart for songs with two singers
hot100df['Singer'] = hot100df['Singer'].str.split(' & ')
hot100df = hot100df.explode('Singer')

# Find the top 20 most common singers and filter by singer
top_artists = hot100df['Singer'].value_counts().head(20).index
filtered_df = hot100df[hot100df['Singer'].isin(top_artists)]
sia = SentimentIntensityAnalyzer()

# Calculate sentiment for each song
filtered_df['Sentiment'] = filtered_df['Lyrics'].apply(lambda lyrics: sia.polarity_scores(lyrics)['compound'])

# Group by Singer and calculate average sentiment
avg_sentiment_by_artist = filtered_df.groupby('Singer')['Sentiment'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(avg_sentiment_by_artist['Singer'], avg_sentiment_by_artist['Sentiment'], color = '#109DAD', edgecolor = 'black')

ax.set_xlabel('Artist')
ax.set_ylabel('Average Sentiment')
plt.xticks(rotation=45, ha='right')
plt.show()