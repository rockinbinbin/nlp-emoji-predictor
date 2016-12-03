from bs4 import BeautifulSoup


def create_emoji_map():

    # emoji_map[UNICODE] = {'name': NAME, 'tags': [tag0, tag1, tag2...], 'sentiment': SENTIMENT}
    emoji_map = {}

    # from http://www.unicode.org/emoji/charts/emoji-list.html
    with open('unicode_consortium_emoji_data.html', 'r') as emojiFile:
        text = emojiFile.read()

    soup = BeautifulSoup(text, "html.parser")

    for row in soup.find('table').find_all('tr'):

        # skip first row
        if row != soup.find('table').find_all('tr')[0]:
            cols = row.find_all('td')

            unicode = cols[2].string.encode('utf-8')
            name = cols[4].string.encode('unicode-escape')

            temp = cols[5].find_all('a')
            tags = []
            for tag in temp:
                tags.append(tag.string.encode('unicode-escape'))

            emoji_map[unicode] = {'name': name, 'tags': tags}

    # from http://kt.ijs.si/data/Emoji_sentiment_ranking/
    with open('emoji_sentiment_ranking.html', 'r') as sentimentFile:
        text = sentimentFile.read()
        
    count = 0
    soup = BeautifulSoup(text, 'html.parser')
    for row in soup.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        unicode = '\U000' + cols[2].string.split('x')[1]
        sentiment = cols[8].string.encode('unicode-escape')

        # if is emoji
        if emoji_map.get(unicode) != None:
            count += 1
            emoji_map[unicode]['sentiment'] = sentiment
    return emoji_map


if __name__ == "__main__":
    create_emoji_map()