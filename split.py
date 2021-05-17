from newspaper import Article
from nltk.tokenize import sent_tokenize

# non closing tags
non_closing_tags = ["area", "base", "br", "col", "command", "embeded", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"]

# split data into sentence
def split_data(data):
    sentences = ""
    for d in data:
        sentences += d['text']
    return sent_tokenize(sentences)

# split document into block
def split_block(data):
    ds, blocked = [], []
    index_block = data[0]['block']
    for d in data:
        if index_block == d['block']:
            ds.append(d)
            continue
        blocked.append(ds[:])
        index_block = d['block']
        ds = [d]
    return blocked

# find tags(<p>, <span id="..">, <div ...>, </p> ...) from html
def find_tags(html, index):
    tags = ''
    while html[index] != '>':
        tags += html[index]; index += 1
    tags += html[index]; index += 1 # add '>'
    return tags, index

# find text(not tags) from html
def find_text(html, index):
    text = ''
    while html[index] != '<':
        if html[index] == '\n': index += 1; continue # remove newline
        text += html[index]; index += 1
    return text, index

# find tag(p, span, div ...) from tags(<p>, <span id="..">, <div ...>, </p> ...
def find_tag(tags):
    if ' ' in tags: # nonsingle open tag (<p id="..">, <span class=".."> ...)
        tag = list(tags.split(' '))[0][1:]
    else: # single open/close tag (<p>, </p> <span> ...)
        tag = tags[1:-1]
    return tag

# find attr(id="..", class="..." ...) from tags(<p>, <span id="..">, <div ...>, </p> ...
def find_attr(tags):
    if ' ' in tags: # if nonsingle tags
        return list(tags[:-1].split(' ')[1:])
    return None

# update stack: pop if closing tag, push if open tag
def update_stack(stack, tag):
    # if close tag, pop tag
    if tag[0] == '/':
        stack.pop()
    # else open tag with closing, push tag
    elif tag not in non_closing_tags:
        stack.append([tag, attr])
    return stack

# update sentence: save texts with all tags and attrs
def update_data(data, stack, text, block):
    if text in "\n\t" or text == ' '*len(text): return data # for empty text
    tags, attrs = [], []
    for tag, attr in stack:
        tags.append(tag); attrs.append(attr)
    data.append({"tag":'>'.join(tags), "attr":attrs, "text":text, "block":block})
    return data

# update block: seperate article into blocks
def update_block(tag, block):
    if tag in ['div', 'p', 'li', 'ul', 'ol', 'h1', 'h2', 'h3']:
        block += 1
    return block

# get article with newspaper from url
url = "https://en.wikipedia.org/wiki/Korea"
url = "https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart"
article = Article(url, keep_article_html=True)
article.download()
article.parse()

# get article's html and text
html, html_text = article.article_html, article.text

# sentence processing
index = 0
block = 0
stack = []
data = [] # list of dictionary with "tag", "attr", "text", "block"
while index < len(html):
    # blank space process
    if html[index] in "\n\t":
        index += 1
        continue
    # if tag
    if html[index] == '<':
        tags, index = find_tags(html, index)
        tag = find_tag(tags)
        attr = find_attr(tags)
        stack = update_stack(stack, tag)
        block = update_block(tag, block)
    # else not tag
    else:
        text, index = find_text(html, index)
        data = update_data(data, stack, text, block)

def update_tag(block, sentences):
    index, index2 = 0, 0 # index for split data (i: row, j: col)
    for i, data in enumerate(block):
        tag, attr, text = data['tag'], data['attr'], data['text']
        while text:
            if text[0] in "\n ": # erase indent
                text = text[1:]
                continue
            if sentences[index][index2] in "\n ": # erase indent
                index2 += 1
                continue
            split = sentences[index][index2:]
            if text == split:
                text = ''
                index += 1; index2 = 0
            elif text[:len(split)] == split:
                text = text[len(split):]
                index += 1; index2 = 0
            elif text == split[:len(text)]:
                index2 += len(text)
                text = ''
            else:
                print("ERROR")
                exit()

# split data at dot
def split_dot(datas, data):
    text = data['text']
    while '.' in text:
        index = text.find('.')
        new_text = text[:index + 1]
        datas.append({"tag":data["tag"], "attr":data["attr"], "text":new_text, "block": data["block"]})
        text = text[index + 1:]
    datas.append({"tag":data["tag"], "attr":data["attr"], "text":text, "block": data["block"]})
    return datas

ds = []
for d in data:
    split_dot(ds, d)

data_block = split_block(ds)
count = 0
for block in data_block:
    if count < 5: count+=1; continue
    sentences = split_data(block)
    
    for b in block:
        print(b['tag'], b['attr'], b['text'], sep='\n', end='\n\n')
    print("======================================================")
    # for sentence in sentences:
    #     print(sentence, end='\n\n')

"""
index = 0
for d in data_with_line:
    d['text'].replace('\n', '')
    if d['line'] == index:
        print(d["text"], end='')
    else:
        index = d['line']
        print(d['text'], end='\n===============\n')
"""

# J.&#160;C. Bach -> J. C. Bach
