# emoji_predictor

####twitter_scraper.py
  - To run `python twitter_scraper.py`
  - Scrapes English tweets with an emoji that are not retweets
  - Writes `id, tweet` to tweets.csv
 

####create_emoji_map.py
  - Creates dictionary of emojis and their unicode, name, tags, and sentiment
  - emoji_map[UNICODE] = {'name': NAME, 'tags': [tag0, tag1, tag2...], 'sentiment': SENTIMENT}
  - Emoji unicode, names, and tags from [Unicode Consortium](http://www.unicode.org/emoji/charts/emoji-list.html)
  - Emoji sentiment from [Novak et. al.] (http://kt.ijs.si/data/Emoji_sentiment_ranking)
 
