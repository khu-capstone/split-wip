class Broker():
    def __init__(self, html):
        self.html = html
        self.index = 0 # Broker index
        self.stack = [] # tag stack
        self.data = [] # structured data with tag, attr, text, block
        self.tag = None
        self.tags = None
        self.attr = None
        self.attrs = None
        self.block = 0 # Borker index for block
        self.text = ''
        # tags with no closing
        self.non_closing_tags = ["area", "base", "br", "col", "command", "embeded", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]
        # tags with article
        self.article_tags = ['div', 'p', 'li', 'ul', 'ol', 'h1', 'h2', 'h3']
        self.process()
    
    def process(self):
        while self.index < len(self.html):
            # blank space process
            if self.html[self.index] in "\n\t":
                self.index += 1
                continue
            # if tag
            if self.html[self.index] == '<':
                self.tag_process()
            # else not tag
            else:
                self.text_process()
    
    def tag_process(self):
        self.update_tags()
        self.update_tag()
        self.update_attr()
        self.update_stack()
        self.update_block()

    def text_process(self):
        self.update_text()
        self.update_data()
    
    # find tags(<p>, <span id="..">, <div ...>, </p> ...) from html
    def update_tags(self):
        self.tags = ''
        while self.html[self.index] != '>':
            self.tags += self.html[self.index]
            self.index += 1
        # add '>'
        self.tags += self.html[self.index]
        self.index += 1

    # find tag(p, span, div ...) from tags(<p>, <span id="..">, <div ...>, </p> ...
    def update_tag(self):
        if ' ' in self.tags: # nonsingle open tag (<p id="..">, <span class=".."> ...)
            self.tag = list(self.tags.split(' '))[0][1:]
        else: # single open/close tag (<p>, </p> <span> ...)
            self.tag = self.tags[1:-1]
  
    # find attr(id="..", class="..." ...) from tags(<p>, <span id="..">, <div ...>, </p> ...
    def update_attr(self):
        if ' ' in self.tags: # if nonsingle tags
            self.attr = list(self.tags[:-1].split(' ')[1:])
        else:
            self.attr = None

    # update stack: pop if closing tag, push if open tag
    def update_stack(self):
        # if close tag, pop tag
        if self.tag[0] == '/':
            self.stack.pop()
        # else open tag with closing, push tag
        elif self.tag not in self.non_closing_tags:
            self.stack.append([self.tag, self.attr])
    
    # update block: seperate article into blocks
    def update_block(self):
        if self.tag in self.article_tags:
            self.block += 1
    
    # find text(not tags) from html
    def update_text(self):
        self.text = ''
        while self.html[self.index] != '<':
            # remove newline
            if self.html[self.index] == '\n':
                self.index += 1
                continue
            self.text += self.html[self.index]
            self.index += 1

    # update sentence: save texts with all tags and attrs
    def update_data(self):
        if self.text in "\n\t" or self.text == ' '*len(self.text):
            return # for empty text
        self.tags, self.attrs = [], []
        for self.tag, self.attr in self.stack:
            self.tags.append(self.tag)
            self.attrs.append(self.attr)
        self.data.append({"tag":'>'.join(self.tags), "attr":self.attrs, "text":self.text, "block":self.block})
