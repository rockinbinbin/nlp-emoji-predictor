import requests
from bs4 import BeautifulSoup

def create_emoji_map():

    emoji_map = {} # emoji_map[UNICODE] = [name, [tag0, tag1, tag2...], sentiment]

    with open('unicode_consortium_emoji_data.html', 'r') as htmlFile:
        text = htmlFile.read()

    soup = BeautifulSoup(text, "html.parser")

    with open('Emoji_Sentiment_Data_v1.0.csv', 'r') as csvFile:
        for row in csvFile:

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

            emoji_map[unicode] = [name, tags]
            print(emoji_map)
            assert 3 == 4

    return emoji_map

if __name__ == "__main__":
    create_emoji_map()