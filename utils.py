# open file
def open_file(path):
    file = open(path, 'r')
    return file

# close file
def close_file(file):
    file.close()