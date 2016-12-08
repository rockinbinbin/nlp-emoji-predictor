# emoji_predictor

To install requirements: `pip install -r requirement.txt`


#### main.py
  - To run: `python main.py PATH_TO_TWEETS_FILE`
  

##Data


####Twitter Scraper
  - To run: `python twitter_scraper.py`
  - Scrapes English tweets with an emoji that are not retweets
  - Writes `id, tweet` to tweets.csv
 

####Scraping Unicode Consortium & Emoji Sentiment Ranking
  - To run: `python create_emoji_map.py`
  - Write a dictionary of emojis and their unicode, name, tags, and sentiment to "emoji_map.txt"
  - emoji_map[UNICODE] = {'name': NAME, 'tags': [tag0, tag1, tag2...], 'sentiment': SENTIMENT}
  - Emoji unicode, names, and tags from [Unicode Consortium](http://www.unicode.org/emoji/charts/emoji-list.html)
  - Emoji sentiment from [Novak et. al.] (http://kt.ijs.si/data/Emoji_sentiment_ranking)
 
