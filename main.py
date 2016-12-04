import argparse
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
# from create_emoji_map import create_emoji_map

def is_hashtag(tok):
    """Returns true if token is a hashtag"""
    if tok[0] == '#':
        return True
    return False


def is_hyperlink(tok):
    """Returns true if token is hyperlink"""
    if 'http' in tok:
        return True
    return False


def is_mention(tok):    # TODO: Should mentions be replace by 'mention' instead of being removed?
    """Returns true if token is mention"""
    if tok[0] == '@':
        return True
    return False

def findMiddleText(start, end, line):
    foundWord = ""
    if line.find(start):
        startAndword = line[line.find(start):line.rfind(end)]
        foundWord = startAndword[len(start):]
        return foundWord

def findMiddletoEndLine(start, line):
    foundWord = ""
    if line.find(start):
        startAndword = line[line.find(start):]
        foundWord = startAndword[len(start):]
        return foundWord

def end_emoji(tweet): # TODO: This is so broken
    """Returns False if there is no emoji at the end of tweet.
    Returns the first emoji at the end of tweet. If the first emoji is a sequence, returns sequence.
    If there are no spaces between the emojis at the end of tweet, separates emojis.
    """
    if '\U000' not in tweet:
        print(tweet)
    else:
        toks = tweet.split(' ')

        if is_hyperlink(toks[:]):
            toks.pop()

        # has emoji at end?
        if '\\U000' not in toks[:]:
            return False, None
        else:
            # find first emoji
            for i in range(len(toks), 0):
                # space between emojis?

                if '\\U000' in toks[i]:
                    emoji = toks[:]
                else:
                    break

            # is emoji_sequence?
            return True, emoji

def baseline(tweets, emoji_maps):
    #takes cleaned tweets
    #appends baseline emoji to end
    assigned_tweets = []
    for tweet in tweets:
        emoji_assigned = False
        for word in tweet.split():
            for emoji_map in emoji_maps:
                tags = emoji_map["tags"]
                for tag in tags.split():
                    if word == tag and emoji_assigned == False:
                        uni = emoji_map["unicode"]
                        print(uni)
                        tweet = tweet + uni
                        assigned_tweets.append(tweet)
                        emoji_assigned = True
        if emoji_assigned == False:
            vs = vaderSentiment(tweet)
            positive = vs["pos"]
            negative = vs["neg"]
            neutral = vs["neu"]
            compound = vs["compound"]
            uni = ""
            if positive > negative:
                uni = "\U0001f60a"
            else:
                uni = "\U0001f622"
            tweet = tweet + uni
            assigned_tweets.append(tweet)
            emoji_assigned = True
    print(assigned_tweets)
    return assigned_tweets

def parse_emoji_map():
    emoji_maps = []
    emoji_map = {}
    with open('emoji_map.txt', 'r') as data:
        for line in data.read().split("\n"):
            if len(line) > 2:
                emoji_map["unicode"] = line.split()[1]
                emoji_map["name"] = findMiddleText("name: ", " sentiment:", line)
                emoji_map["sentiment"] = findMiddleText("sentiment: ", " tags:", line)
                emoji_map["tags"] = findMiddletoEndLine("tags: ", line)
                emoji_maps.append(emoji_map)
                emoji_map = {}
    return emoji_maps

def main():
    tweets = ["hi i love you", "sad tweet", "this tweet is great", "i like nlp", "happy tweet"]
    emoji_maps = parse_emoji_map()
    baseline(tweets, emoji_maps)

    # parser = argparse.ArgumentParser()
    # parser.add_argument('tweets')
    # args = parser.parse_args()

    # tweet_count = 0
    # set_count = 0

    # with open(args.tweets, 'r') as inFile:
    #     for line in inFile:
    #         tweet_count += 1
    #         tweet_id, tweet = line.split(',', 1)

    #         has_end_emoji, emoji = end_emoji(tweet)

    #         if has_end_emoji:
    #             set_count += 1
    #             toks = tweet.split(' ')

    #             for i in range(len(toks), 0):
    #                 tok = toks[i]

    #                 # TODO: Should emojis within body of tweet be eliminated?
    #                 # TODO: ie. "Rachel EMOJI is so happy EMOJI"
    #                 if is_hashtag(tok) or is_hyperlink(tok) or is_mention(tok):
    #                     toks.remove(tok)

    # emoji_map = create_emoji_map()

    # TODO: Baseline
    # if keyword, map keyword to emoji
    # if not, get sentiment of tweet and assign most used emoji for that sentiment

    # TODO: Keyword Matching

    # TODO: Sentiment Analysis - VADER
    # return sentiment of tweet
    # or return diff between tweet sentiment and emoji sentiment
        # goal is the find the optimal emoji (least amount of difference)

    # TODO: WSD

    # print("Tweets with Emojis: " + tweet_count)
    # print("Tweets with Emojis at End: " + set_count)

if __name__ == "__main__":
    main()
