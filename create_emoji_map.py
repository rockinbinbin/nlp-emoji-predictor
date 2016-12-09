from bs4 import BeautifulSoup
# run python create_emoji_map.py once to create text files – don't call directly from project.
# writes to "emoji_map.txt" a map for unicode, name, sentiment, and tags
"""Run python create_emoji_map.py once to create text files.
Writes to "emoji_map.txt" a map for unicode, name, sentiment, and tags."""

def create_emoji_map():
    # emoji_map[UNICODE] = {'name': NAME, 'tags': [TAG0, TAG1, TAG2...], 'sentiment': SENTIMENT}
    emoji_map = {}

    # from http://www.unicode.org/emoji/charts/emoji-list.html
    with open('docs/unicode_consortium_emoji_data.html', 'r') as emojiFile:
        text = emojiFile.read()

    soup = BeautifulSoup(text, "html.parser")

    for row in soup.find('table').find_all('tr'):

        # skip first row
        if row != soup.find('table').find_all('tr')[0]:
            cols = row.find_all('td')

            unicode = cols[2].string.encode('utf-8').lower()
            # TODO: include flags
            if unicode.count('u') == 1:    # exclude emoji sequences
                name = cols[4].string.encode('unicode-escape')

                temp = cols[5].find_all('a')
                tags = []
                for tag in temp:
                    tags.append(tag.string.encode('unicode-escape'))

                emoji_map[unicode] = {'name': name, 'tags': tags}

    # from http://kt.ijs.si/data/Emoji_sentiment_ranking/
    with open('docs/emoji_sentiment_ranking.html', 'r') as sentimentFile:
        text = sentimentFile.read()

    count = 0
    soup = BeautifulSoup(text, 'html.parser')
    for row in soup.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        unicode = '\U000' + cols[2].string.split('x')[1]
        sentiment = float(cols[8].string.encode('unicode-escape'))

        # if is emoji
        if emoji_map.get(unicode) != None:
            count += 1
            emoji_map[unicode]['sentiment'] = sentiment
    return emoji_map

def write_emoji_map_to_file(emoji_map):
    outFile = open("emoji_map.txt", 'w')
    for uni in emoji_map:
        value = emoji_map[uni]

        outFile.write("unicode: ")
        outFile.write(uni)
        outFile.write(" ")
        if "name" in value:
            outFile.write("name: ")
            outFile.write(value["name"])
            outFile.write(" ")

        if "sentiment" in value:
            outFile.write("sentiment: ")
            outFile.write(value["sentiment"])
            outFile.write(" ")

        if "tags" in value:
            outFile.write("tags: ")
            for tag in value["tags"]:
                outFile.write(tag)
                outFile.write(" ")
        outFile.write("\n")

if __name__ == "__main__":
    emoji_map = create_emoji_map()
    write_emoji_map_to_file(emoji_map)
