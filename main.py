from article import Article
from broker import SentenceBroker

# open file
def open_file(path):
    file = open(path, 'r')
    return file

# close file
def close_file(file):
    file.close()

# get html from url
def get_html_from_url(url):
    article = Article(url)
    return article.html

# make structured html text from pure html
def get_sentence_broker(html):
    return SentenceBroker(html)

# sb.get_sentences()
# get all sentences (line, tag, text)
# [{'line': 338, 'tag': 'p', 'text': 'Further reading'}, ...]

# sb.get_sentences_with_tag(<tag>)
# get sentences with tag (line, tag, text)
# sb.get_sentences_with_tag('li')
# [{'line': 147, 'tag': 'li', 'text': 'Raimund Leopold (17 June&#160;&#8211; 19 August 1783)'}, ...]

# sb.get_sentences_without_tag(<tag>)
# get sentences without tag (line, tag, text)
# sb.get_sentences_without_tag('p')
# [{'line': 147, 'tag': 'li', 'text': 'Raimund Leopold (17 June&#160;&#8211; 19 August 1783)'}, ...]

def process_tag(html, tag):
    f = open("ol_wiki.csv", 'a')
    prevs = []
    for sentence in sb.get_sentences_with_tag(tag):
        prev = sb.get_previous_sentence(sentence, tag)
        uppr = sb.get_upper_sentence(sentence, tag)
        # print('uppr:', uppr)
        # print('prev:', prev)
        # print('orig:', sentence['text'])
        # print("========")
        if not prev or not uppr:
            continue
        elif prev == uppr:
            continue
        elif prev in prevs:
            continue
        else:
            f.write(prev + '\n')
        prevs.append(prev)
    f.close()
        

if __name__ == "__main__":
    # wikipedia url datasets
    # https://www.kaggle.com/residentmario/wikipedia-article-titles
    baseurl = "https://en.wikipedia.org/wiki/"
    filename = "titles.txt"
    # open file
    wikifile = open_file(filename)
    # process file
    line = wikifile.readline()
    index = 0
    wanted = 0
    while line:
        if wanted > 0:
            index += 1
            wanted -= 1
            line = wikifile.readline()
            continue
        # get html from url
        try:
            url = baseurl + line.split()[0]
            print(index, url)
            html = get_html_from_url(url)
            # get sentence broker from html
            sb = get_sentence_broker(html)
            # ul process
            process_tag(html, 'ol')
            line = wikifile.readline()
            index += 1
        except:
            line = wikifile.readline()
            index += 1
    # close file
    close_file(wikifile)
