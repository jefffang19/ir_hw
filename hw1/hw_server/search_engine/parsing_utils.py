import json

# for parsing xml file
from bs4 import BeautifulSoup
# read a xml file from path
# return a list of found tags
# use tags.string to get str
def xml_reader(path, target_tag):
    f = open(path,'r',encoding="utf-8")

    raw = f.read()
    soup = BeautifulSoup(raw, 'lxml')
    tags = soup.find_all(target_tag)
    return tags

# tokenlize a string from xml and store as a array (len = number of articles)
# the element of array looks like
# { 'sentence' : 'I like apple',
#   'words' : ['I', 'like', 'apple']}
def xml_string_parser(raw):
    d = {'sentence' : raw,
         'words' : []}
    
    for i in range(len(raw.split())):
        d['words'].append( [raw.split()[i], i] )

    return d


# read a json file from path
def json_reader(path):
    input_file = open(path,'r')
    input_raw = input_file.read()
    input_json = json.loads(input_raw)
    
    return input_json

# parse a json file and store as a array (len = number of articles)
# the element of array looks like
# { 'sentence' : 'I like apple',
#   'words' : ['I', 'like', 'apple']}
def json_parser(json_dict):
    result = []

    for i in json_dict:
        sentence = []
        for c in i['tweet_text']:
            if(c.isascii()):
                sentence.append(c)
                
        sentence = ''.join(sentence)
        
        element = {}
        words = []
        pos = []
        element['sentence'] = sentence
        for j in range(len(sentence.split())):
            words.append( [sentence.split()[j], j] )
        element['words'] = words
        
        result.append(element)
    
    return result

def remove_puncuation(word_list):
    import string
    
    en_titles = ['Mr.', 'Mrs.', 'Dr.', 'Prof.','Hon.']

    for i in range(len(word_list)):
        if word_list[i][0] in en_titles:
            continue
        elif len(word_list[i][0])==2 and word_list[i][0][0].isupper():
            continue
        else:
            for j in string.punctuation:
                word_list[i][0] = word_list[i][0].replace(j, '')
       
    # remove blank string from the list
    word_list = [i for i in word_list if i[0] != ""]
    
    return word_list


def words_to_lower(word_list):
    return [ [i[0].lower(), i[1]] for i in word_list]


def remove_stopords(word_list, stopword_path = 'D:\\work\\ir_hw\\hw1\\stop_words.txt'):
    f = open(stopword_path)
    stop_words = f.read().split('\n')
    # now we create a new word set without the stop words
    words = [ [word_list[i][0], word_list[i][1]] for i in range(len(word_list)) if word_list[i][0] not in stop_words]
    
    return words


def stemming(word_list):
    from nltk.stem import PorterStemmer 

    ps = PorterStemmer() 

    for i in range(len(word_list)):
        word_list[i][0] = ps.stem(word_list[i][0])
        
    return word_list


# return type
# { 'sentence' : '\n I like apple',
#   'words' : [['I',1], ['like',2], ['apple',3]],
# }
def data_processor(input_path, mode = 'json'):
    if mode == 'json':
        raw_json = json_reader(input_path)
        articles = json_parser(raw_json)
        for i in articles:
            # process words list
            i['words'] = stemming(remove_stopords(words_to_lower(remove_puncuation(i['words']))))
        
        return articles

    elif mode == 'xml':
        tags = xml_reader(input_path, 'p')
        abstract = xml_string_parser(tags[3].string)
        abstract['words'] = stemming(remove_stopords(words_to_lower(remove_puncuation(abstract['words']))))

        return abstract

        
