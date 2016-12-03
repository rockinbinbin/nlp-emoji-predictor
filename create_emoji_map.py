from bs4 import BeautifulSoup


def create_emoji_map():

    # emoji_map[UNICODE] = {'name': NAME, 'tags': [tag0, tag1, tag2...], 'sentiment': SENTIMENT}
    emoji_map = {}

    # from http://www.unicode.org/emoji/charts/emoji-list.html
    with open('unicode_consortium_emoji_data.html', 'r') as htmlFile:
        text = htmlFile.read()

    soup = BeautifulSoup(text, "html.parser")

    for row in soup.find('table').find_all('tr'):

        # skip first row
        if row != soup.find('table').find_all('tr')[0]:
            cols = row.find_all('td')

            unicode = cols[2].string.encode('unicode-escape')
            name = cols[4].string.encode('unicode-escape')

            temp = cols[5].find_all('a')
            tags = []
            for tag in temp:
                tags.append(tag.string.encode('unicode-escape'))

            emoji_map[unicode] = {'name': name, 'tags': tags}
            print(emoji_map)
            assert 3 == 4

    # from http://kt.ijs.si/data/Emoji_sentiment_ranking/
    with open('emoji_sentiment_ranking.html', 'r') as sentimentFile:
        for row in sentimentFile:

    return emoji_map


if __name__ == "__main__":
    create_emoji_map()