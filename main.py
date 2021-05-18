from article import Article
from broker import Broker

# get url
url = "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"

# get html from url
article = Article(url)
html = article.html

# make structured html text from pure html
sentence = Broker(html)


print(sentence.data)