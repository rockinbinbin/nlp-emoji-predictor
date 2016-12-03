import argparse

from create_emoji_map import create_emoji_map

def is_hashtag(tok):
    if tok[0] == '#':
        return True
    return False


def is_hyperlink(tok):
    if 'http' in tok:
        return True
    return False


def is_mention(tok):
    if tok[0] == '@':
        return True
    return False


def end_emoji(tweet): #TODO: This is so broken
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweets')
    args = parser.parse_args()

    tweet_count = 0
    set_count = 0

    with open(args.tweets, 'r') as inFile:
        for line in inFile:
            tweet_count += 1
            tweet_id, tweet = line.split(',', 1)

            has_end_emoji, emoji = end_emoji(tweet)

            if has_end_emoji:
                set_count += 1
                toks = tweet.split(' ')

                for i in range(len(toks), 0):
                    tok = toks[i]

                    if is_hashtag(tok) or is_hyperlink(tok) or is_mention(tok):
                        toks.remove(tok)

    emoji_map = create_emoji_map()

    # TODO: Keyword Matching

    # TODO: Sentiment Analysis - VADER

    # TODO: WSD

    print("Tweets with Emojis: " + tweet_count)
    print("Tweets with Emojis at End: " + set_count)

if __name__ == "__main__":
    main()
