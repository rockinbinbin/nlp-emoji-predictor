import argparse

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

def end_emoji(tweet):
    toks = tweet.split(' ')

    # has emoji at end
    toks[:]
    return False, None
    # is emoji_sequence
    return True, emoji


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tweets')
    args = parser.parse_args()


    with open(args.tweets, 'r') as inFile:
        for line in inFile:
            tweet_id, tweet = line.split(',', 1)
            has_end_emoji, emoji = end_emoji(tweet)
            if has_end_emoji:
                toks = tweet.split(' ')

                for i in range(len(toks), 0):
                    tok = toks[i]

                    if is_hashtag(tok) or is_hyperlink(tok) or is_mention(tok):
                        toks.remove(tok)

if __name__ == "__main__":
    main()
