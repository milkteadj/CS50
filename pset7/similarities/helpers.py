from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""
    # TODO
    list_both = list(set(a.split("\n")).intersection(set(b.split("\n"))))
    return list_both


def sentences(a, b):
    """Return sentences in both a and b"""
    # TODO
    return list(set(sent_tokenize(a)).intersection(sent_tokenize(b)))


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    # return substrings of a with regard to its end.
    SetA = set()
    for i in range (len(a) - (n-1)):
        SetA.add(a[i: i + n])
    # do the same to B.
    SetB = set()
    for i in range(len(b) - (n-1)):
        SetB.add(b[i: i + n])

    # find the intersection of the two sets and turn it into a list
    return list(SetA.intersection(SetB))

