

# implement the Levenshtein (edit distance) algorithm
# taken from: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def edit_distance(s1, s2):
    if len(s1) < len(s2):
        return edit_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


class MaliciousnessAnalysis:
    def __init__(self):
        self.found_word_list = []
        self.similar_brand_list = []
        self.similar_keyword_list = []

    def analyze(self, word):
        if word not in open('../input/brands.txt').read() \
                and word not in open('../input/keywords.txt').read():
            self.found_word_list.append(word)
        else:
            for brand in open('../input/brands.txt').read():
                if edit_distance(word.lower(), brand.lower()) < 2:
                    self.similar_brand_list.append(word)
            for keyword in open('../input/keywords.txt').read():
                if edit_distance(word.lower(), keyword.lower()) < 2:
                    self.similar_keyword_list.append(word)
        return self.found_word_list, self.similar_brand_list, self.similar_keyword_list
