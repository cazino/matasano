from collections import defaultdict
import operator


class EnglishScorer(object):
    """Scores a text so that
    an english text get a higher score.
    """

    #def __init__(self, text):
    #    self.text = text

    def score(self, text):
        """Scores plain english text  with
        "ETAOIN SHRDLU" occurences
        """
        text = text.upper()
        ref = "ETAOINSHRDLU"
        occurences = defaultdict(int)
        for char in text:
            occurences[char] += 1
        sorted_occ = sorted(occurences.items(),
                            key=operator.itemgetter(1),
                            reverse=True)
        sorted_char = [x for (x, y) in sorted_occ if x != " "]
        distance = 0
        restricted_sorted_char = sorted_char[:12]
        for char in restricted_sorted_char:
            try:
                tmp_dist = abs(restricted_sorted_char.index(char) -
                               ref.index(char))
            except ValueError:
                tmp_dist = 12
            distance += tmp_dist
        if restricted_sorted_char:
            return distance / (12 * len(restricted_sorted_char))
        return 1
