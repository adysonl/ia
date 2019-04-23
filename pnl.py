import urllib3 as lib

def get_text(url):
    lib.disable_warnings()
    http = lib.PoolManager()
    response = http.request('GET', target_url)
    return response.data.decode('utf-8')

def text_to_list(text):
    signs = '!.?*-:,;!@#$%&/\|+'
    space = ' '
    for sign in signs:
        text = text.replace(sign, space + sign + space)   
    list = text.lower().split()
    return list

def get_prev_words(text, index, num_words):
    words = []
    for i in range(num_words):
        words += [text[index]]
        index -= 1
    words.reverse()
    return words
        
def predict_words(text, sentence, option): #option == 2 ? bigram : option == 3 ? trigram : ...
    count = 0
    next_words = []
    probs = []
    result = []
    num_words = int(option) - 1 
    words  = sentence[-num_words:]
    for i in range(len(text)):
        if i >= num_words:
            if get_prev_words(text, i, num_words) == words: 
                count += 1
                if i + 1 < len(text):
                    next = text[i+1]
                    if next not in next_words: #if it's not the last word
                        next_words.append(next)
                        probs.append(1)
                    else:
                        next_index = next_words.index(next)
                        probs[next_index] += 1
    for i in range(3):    
        if len(probs) > 0:
            max_prob = max(probs)
            max_i = probs.index(max_prob)
            result.append([next_words[max_i], max_prob])

            del probs[max_i]
            del next_words[max_i]
    
    return [count, result]



#target_url = 'http://norvig.com/ngrams/shakespeare.txt'
target_url = 'https://raw.githubusercontent.com/yurimalheiros/ainotebooks/master/nlp/machadodeassiscorpus.txt'

words = text_to_list(get_text(target_url))
word = ''
while True:
    option = input('for bigram type 2, trigram 3, close X: ')
    if option.upper() == 'X':
        break
    elif option == '2' or option == '3':
        input_words = input('sentence: ').split(' ')
        print('count = ' + str(predict_words(words, input_words, option)))



"""

def count(text, word):
    word.lower()
    count = 0
    for w in text:
        if w == word:
            count += 1
    return count

def bi_count(text, word):
    count = 0
    next_words = []
    probs = []
    result = []
    for i in range(len(text)):
        if text[i] == word: 
            count += 1
            if i + 1 < len(text):
                next = text[i+1]
                if next not in next_words: #if it's not the last word
                    next_words.append(next)
                    probs.append(1)
                else:
                    next_index = next_words.index(next)
                    probs[next_index] += 1
    for i in range(3):    
        if len(probs) > 0:
            max_prob = max(probs)
            max_i = probs.index(max_prob)
            result.append([next_words[max_i], max_prob])

            del probs[max_i]
            del next_words[max_i]
    
    return count, result

def tri_count(text, words):
    count = 0
    next_words = []
    probs = []
    result = []
    for i in range(len(text)):
        if i > 0:
            if [text[i-1],text[i]] == words: 
                count += 1
                if i + 1 < len(text):
                    next = text[i+1]
                    if next not in next_words: #if it's not the last word
                        next_words.append(next)
                        probs.append(1)
                    else:
                        next_index = next_words.index(next)
                        probs[next_index] += 1
    for i in range(3):    
        if len(probs) > 0:
            max_prob = max(probs)
            max_i = probs.index(max_prob)
            result.append([next_words[max_i], max_prob])

            del probs[max_i]
            del next_words[max_i]
    
    return [count, result]

while True:
    option = input('for bigram type 2, trigram 3, close X: ')
    if option == 'X':
        break
    else:
        input_words = input('sentence: ').split(' ')
        if option == '2':
            print('count = ' + str(bi_count(words, input_words[-1])))
        elif option == '3':
            print('count = ' + str(tri_count(words, input_words[-2:])))
"""
