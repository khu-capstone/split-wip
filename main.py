from article import Article
from broker import SentenceBroker
from utils import open_file, close_file
import nltk

def process(sb, tag):
    rs = []
    for sentence in sb.get_sentences_with_tag(tag):
        orig = sentence['text']
        prev = sb.get_previous_sentence(sentence, tag)
        uppr = sb.get_upper_sentence(sentence, tag)
        print('uppr:', uppr)
        print('prev:', prev)
        print('orig:', sentence['text'])
        print("========")
        continue
        if not prev or not uppr or prev == uppr:
            continue
        r = ''
        if prev[-1] == ":" or prev[-2:] == ' :':
            r = prev + ' ' + orig
        elif prev[-2:] == ': ':
            r = prev + orig
        else:
            r = orig
        rs.append(r)
    return rs

if __name__ == "__main__":
    # baseurl = ''
    # baseurl for wiki
    baseurl = "https://en.wikipedia.org/wiki/"
    
    filename = "titles.txt"
    tag = 'ul'
    
    rfile = open_file(filename)
    line = rfile.readline()
    for _ in range(126):
        line = rfile.readline()
    while line:
        try:
            url = baseurl + line.split('\n')[0]
            print(url)
            article = Article(url)
            html = article.html
            sb = SentenceBroker(html)
            rs = process(sb, tag)
            # print(rs)
        except KeyboardInterrupt:
            break
        except:
            pass
        line = rfile.readline().split()[0]
    close_file(rfile)

from openie import StanfordOpenIE
with StanfordOpenIE() as client:
    for text in rs:
        print('Text: %s.' % text)
        for triple in client.annotate(text):
            print('|-', triple)