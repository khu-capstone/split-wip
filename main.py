from article import Article
from broker import SentenceBroker

# get url
url = "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"
url = "https://en.wikipedia.org/wiki/COVID-19"

# get html from url
article = Article(url)
html = article.html

# make structured html text from pure html
sb = SentenceBroker(html)

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

s = sb.get_sentences()
ul = sb.get_sentences_with_tag('ul')
ol = sb.get_sentences_with_tag('ol')
ulol = ul + ol

# get previous header sentence
for u in ulol:
    prev = sb.get_previous_sentence(u)
    uppr = sb.get_upper_sentence(u)
    print('orig: ', u['text'])
    print('uppr: ', uppr['text'])
    print('prev: ', prev['text'])
    print("========")