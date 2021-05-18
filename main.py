from article import Article
from broker import Broker

# get url
url = "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"

# get html from url
article = Article(url)
html = article.html

# sentence processing
sentence = Broker(html)


print(sentence.data)