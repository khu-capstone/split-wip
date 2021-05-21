from article import Article
from broker import SentenceBroker

# get url
url = "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"

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
s = sb.get_sentence(140)

# get previous sentence
# for u in ul:
#     tag = u['tag']
#     index = u['line']
#     while True:
#         s = sb.get_sentence(index)
#         if tag not in s['tag']:
#            break
#         index -= 1
#     print(u)
#     print(s)
#     print("========")

# get previous header sentence
for u in ul:
    tag = u['tag']
    index = u['line']
    while True:
        s = sb.get_sentence(index)
        if tag not in s['tag']:
            if 'h1' in s['tag'] or 'h2' in s['tag'] or 'h3' in s['tag'] or 'h4' in s['tag'] or 'h5' in s['tag'] or 'h6' in s['tag']:
                break
        index -= 1
    print(u)
    print(s)
    print("========")