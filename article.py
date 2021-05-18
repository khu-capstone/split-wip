from newspaper import Article as Art

# get article from url with newspaper3k
# html: article with html format
# text: only text
class Article():
    def __init__(self, url):
        self.url = url
        self.article = Art(self.url, keep_article_html=True)
        self.download()
        self.parse()
        self.html = self.article.article_html
        self.text = self.article.text
    
    def download(self):
        self.article.download()
    
    def parse(self):
        self.article.parse()
