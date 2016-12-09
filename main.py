import argparse
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

from tweet_processing import *


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


# TODO
def keyword_matching():
    """Returns list of len(num_emojis) which indicates whether tweet has a keyword for each emoji """


def baseline(tweets, emoji_maps):
    """Takes cleaned tweets. Returns list of baseline predictions"""
    assigned_emojis = list()

    for tweet in tweets:
        emoji_assigned = False

        for word in tweet.split():

            for emoji_map in emoji_maps:

                tags = emoji_map["tags"]

                for tag in tags.split():

                    if word == tag and emoji_assigned == False:
                        uni = emoji_map["unicode"]
                        print(tag)
                        print(uni)
                        assigned_emojis.append(uni.lower())
                        emoji_assigned = True

        if emoji_assigned == False:
            vs = vaderSentiment(tweet)
            positive = vs["pos"]
            negative = vs["neg"]
            neutral = vs["neu"]
            compound = vs["compound"]

            if positive > negative:
                uni = "\u0001f60a"  # TODO: how were these emojis picked?
            else:
                uni = "\u0001f622"

            assigned_emojis.append(uni)

            emoji_assigned = True

    return assigned_emojis


def parse_emoji_map():
    emoji_maps = list()
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


def sentiment_analysis(tweet):
    """Returns the sentiment of the tweet from -1 to 1"""
    vs = vaderSentiment(tweet)
    pos = vs["pos"]
    neg = vs["neg"]
    neu = vs["neu"]

    # find highest scoring sentiment
    highest = max(pos, neg, neu)

    if highest == neg:
        # negate value and then add to dict
        highest *= -1
    else:
        # neutral value = 0.0 and add to dict
        highest = 0.0

    return highest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweets')   # path to dataset
    args = parser.parse_args()

    emoji_maps = parse_emoji_map()

    tweet_count = 0

    tweets = list()         # tweets = [[tweet1, num_hashtags1, num_mentions1], [tweet2, num_hashtags2, num_mentions2]]
    tweets_gold = list()    # end_emojis for tweets
    emoji_count = {}        # emoji_count[EMOJI] = number of times emoji is end emoji

    with open(args.tweets, 'r') as inFile:
        for line in inFile:
            tweet_count += 1
            process_tweet(line, tweets, tweets_gold, emoji_count)

    # split data 4/5 training, 1/5 test
    num_tweets = len(tweets)
    num_training = int(num_tweets * 4/float(5))

    print("Tweets with Emojis: " + str(tweet_count))
    print("Tweets with Emojis at End: " + str(num_tweets))

    train_tweets = tweets[:num_training]
    train_gold = tweets_gold[:num_training]

    test_tweets = tweets[num_training:]
    test_gold = tweets_gold[num_training:]

    # create feature vectors
    train_fv = list()
    test_fv = list()

    # for tweet in train_tweets:
    #     fv = list()
    #     fv.append(tweet[1])    # num_hashtags
    #     fv.append(tweet[2])    # num_mentions
    #
    #     # TODO: keyword matching
    #
    #     # sentiment
    #     # TODO: Or list of diff between tweet sentiment and emoji sentiment?
    #     fv.append(sentiment_analysis(tweet[0]))
    #
    #     # TODO: word vectors


    # train decision tree
    # clf = DecisionTreeClassifier()
    # clf = clf.fit(train_fv, train_gold)
    #
    # # make predictions
    # predictions = clf.predict(test_fv)
    #
    # # baseline
    # base_predictions = baseline([tweet[0] for tweet in test_tweets], emoji_maps)
    #
    # # evaluate accuracy of baseline
    # assert len(base_predictions) == len(test_gold)
    # assert len(predictions) == len(test_gold)
    #
    # base_correct = 0
    # pred_correct = 0
    #
    # for i in range(0, len(test_tweets)):
    #     if base_predictions[i].lower() == test_gold[i].lower():
    #         base_correct += 1
    #     if predictions[i].lower() == test_gold[i].lower():
    #         pred_correct += 1
    #
    # base_accuracy = base_correct / float(len(test_tweets))
    # pred_accuracy = pred_correct / float(len(test_tweets))
    #
    # print("Baseline Accuracy: " + str(base_accuracy))
    # print("Prediction Accuracy: " + str(pred_accuracy))

if __name__ == "__main__":
    main()
