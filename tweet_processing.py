import re

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


def is_mention(tok):
    """Returns true if token is mention"""
    if tok[0] == '@':
        return True
    return False


def is_punctuation(tok):
    """Returns true if token is punctuation"""
    pattern = re.compile('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )')
    if pattern.match(tok):
        return True
    return False


def is_emoji(tok):
    """Returns true if token is emoji"""
    if '\U' in tok:
        return True
    return False


def end_emoji(tweet):
    """Returns False if there is no emoji at the end of tweet.
    Returns the first emoji at the end of tweet. If the first emoji is a sequence, returns sequence.
    If there are no spaces between the emojis at the end of tweet, separates emojis.
    """
    if '\u' not in tweet:
        print(tweet + ' has no emoji')
        return False, None
    else:
        temp = tweet.split(' ')
        toks = list()
        for tok in temp:
            if len(tok.split('\u')) > 1:
                emojis = tok.split('\u')
                for e in emojis:
                    if e:
                        toks.append('\u' + e)
            else:
                toks.append(tok)

        if is_hyperlink(toks[:]):
            toks.pop()

        # has emoji at end?
        if '\u' not in toks[-1]:
            return False, None
        else:
            for i in range(len(toks) - 1, 0, -1):
                if '\u' in toks[i]:
                    emoji = toks[i]
                else:
                    break
                # TODO: handle flags

            return True, emoji.lower()


def process_tweet(line, tweets, tweets_gold, emoji_count):
    """Returns nothing.
    Appends cleaned tweet, num_hashtags, and num_mentions to tweets.
    Appends the end emoji to tweets_gold.
    Updates the emoji_count dictionary."""

    tweet_id, tweet = line.split(',', 1)
    tweet = tweet.rstrip('"\n').lstrip('"')

    # add space before & after each punctuation mark
    tweet = re.sub('(?<! )(?=[.,!?()])|(?<=[.,!?()])(?! )', r' ', tweet)

    has_end_emoji, emoji = end_emoji(tweet)

    if has_end_emoji:
        toks = tweet.rstrip().split(' ')

        num_mentions = 0
        num_hashtags = 0

        for i in range(len(toks), 0):
            tok = toks[i]

            if is_hashtag(tok):
                num_hashtags += 1
                toks.remove(tok)
            elif is_mention(tok):
                num_mentions += 1
                toks.remove(tok)
            elif is_hyperlink(tok) or is_emoji(tok):
                toks.remove((tok))

        tweets.append([' '.join(toks), num_hashtags, num_mentions])

        tweets_gold.append(emoji)

        if emoji_count.get(emoji):
            emoji_count[emoji] += 1
        else:
            emoji_count[emoji] = 1