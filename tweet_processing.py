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
                # TODO: Handle emoji sequences

            return True, emoji