import itertools
from HTMLParser import HTMLParser
from nltk import WordPunctTokenizer
import string


INPUT_NAMES = [ 'karenina.htm', 'rebirth.htm', 'wandp.htm', 'wandp1.htm', 'wandp2.htm', 'wandp3.htm', 'wandp4.htm' ]

class TolstojParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.inside_dd = False
        self.bgrams = {}
        self.sorted_bgrams = []
        self.tokenizer = WordPunctTokenizer()
        self.token_count = 0


    def handle_starttag(self, tag, attrs):
        if tag == "dd":
            self.inside_dd = True
        else:
            self.inside_dd = False


    def handle_data(self, data):
        if self.inside_dd:
            tokens = self.tokenizer.tokenize(unicode(data, 'utf-8').lower())
            for t1, t2 in itertools.izip(tokens, tokens[1:]):
                self.token_count += 1

                if (t1[0] in string.punctuation) or (t2[0] in string.punctuation):
                    continue

                key = t1.encode('utf-8') + ' ' + t2.encode('utf-8')
                if self.bgrams.has_key(key):
                    self.bgrams[key] += 1
                else:
                    self.bgrams[key] = 1

    def dump_bgrams(self, output_name):
        output = open(output_name, 'wb')
        pickle.dump(self.bgrams, output)
        output.close()


    def make_sorted_bgrams(self):
        self.sorted_bgrams = sorted(self.bgrams.items(), key=lambda x: x[1], reverse=True)

    def print_sorted_bgrams(self):
        for key, count in self.sorted_bgrams:           
            print key, count


if __name__ == '__main__':
    parser = TolstojParser()
    for name in INPUT_NAMES:
        text = open(name).read()
        parser.feed(text)

    print 'Number of tokens:', parser.token_count
    parser.make_sorted_bgrams()
    parser.print_sorted_bgrams()
