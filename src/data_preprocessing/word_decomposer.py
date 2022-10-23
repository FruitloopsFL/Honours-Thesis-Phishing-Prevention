import enchant


# returns a list of substrings for a given string
# only considers substrings with length > 3
def get_all_substrings(str_to_check):
    length = len(str_to_check)
    max_ = length - 3
    return [str_to_check[i: j+1] for i in range(max_) for j in range(i+3, length)]


class WordDecomposer:
    def __init__(self):
        self.dict = enchant.Dict('en_US')
        self.word_list = []

    # TODO: remove false positives - order substrings by length?
    def analyze(self, compound_word):
        word_no_digits = ''.join([i for i in compound_word if not i.isdigit()])
        if self.dict.check(word_no_digits):
            self.word_list.append(word_no_digits)
        else:
            substrings = get_all_substrings(word_no_digits)
            for sub_word in substrings:
                if self.dict.check(sub_word):
                    self.word_list.append(sub_word)
        return self.word_list
