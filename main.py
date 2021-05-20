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
