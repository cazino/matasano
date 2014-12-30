from collections import defaultdict
import operator


class EnglishScorer(object):
    """Scores a text so that
    an english text get a low score.
    A text in another language or in a non langugage
    should get a higher score.
    """

    def _distance(self, chars):
        ref = "ETAOINSHRDLU"
        distance = 0
        for char in chars:
            try:
                tmp_dist = abs(chars.index(char) -
                               ref.index(char))
            except ValueError:
                tmp_dist = 12
            distance += tmp_dist
        if chars:
            return distance / (12 * len(chars))
        return 1

    def score(self, text):
        """Scores plain english text  with
        "ETAOIN SHRDLU" occurences
        """
        text = text.upper()
        occurences = defaultdict(int)
        for char in text:
            occurences[char] += 1
        sorted_occ = sorted(occurences.items(),
                            key=operator.itemgetter(1),
                            reverse=True)
        sorted_char = [x for (x, y) in sorted_occ if x != " "]
        return self._distance(sorted_char[:12])
