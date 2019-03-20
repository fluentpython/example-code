"""
Sentence: iterate over words using a generator expression
"""

# BEGIN SENTENCE_GENEXP
import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
# END SENTENCE_GENEXP


def main():
    import sys
    import warnings
    try:
        filename = sys.argv[1]
        word_number = int(sys.argv[2])
    except (IndexError, ValueError):
        print('Usage: %s <file-name> <word-number>' % sys.argv[0])
        sys.exit(1)
    with open(filename, 'rt', encoding='utf-8') as text_file:
        s = Sentence(text_file.read())
    for n, word in enumerate(s, 1):
        if n == word_number:
            print(word)
            break
    else:
        warnings.warn('last word is #%d, "%s"' % (n, word))

if __name__ == '__main__':
    main()
