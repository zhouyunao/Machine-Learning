import os
import re
import csv
from collections import Counter

def stop_check(text):
    stoplist = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    if text in stoplist:
        return True
    else:
        return False
def main():
    f_in = open('sms_train.tsv','r')
    lines =[]
    lines = f_in.readlines()
    f_in.close()
    f_out = open('train.csv','w')
    ham_dict = list()
    spam_dict = list()
    word_list = list()

    for i in lines:
        tmp = i.strip().split('\t')

        if tmp[0] == 'ham':
            for t in re.split(r'\s|\,|\.|\?|\n|\(|\)|\!|\+|\=|\/', tmp[1].lower()):
                ham_dict.append(t)
        else:
            for t in re.split(r'\s|\,|\.|\?|\n|\(|\)|\!|\+|\=|\/', tmp[1].lower()):
                if t.isalpha() and stop_check(t)== False:
                    spam_dict.append(t)

    spam_counter = Counter(spam_dict)
    for word, count in spam_counter.most_common(2000):
        if len(word) > 1:
            # pass
            word_list.append(word)
    stock = 'reply|send|text|txt|[0-9]{11}|pound|call|tone|£|money|bill|buy|money|@|free|http|www'
    stock = stock.split('|')
    for i in stock:
        if i in word_list:
            pass
        else:
            word_list.append(i)
    print (word_list)
    stock_out = open('stock.csv','w')
    writer_s = csv.writer(stock_out,lineterminator='\n')
    writer_s.writerow(word_list)
    writer = csv.writer(f_out,lineterminator='\n')
    for i in lines:
        tmp = i.strip().split('\t')
        feature = []
        for c in word_list:
            if re.search(c,tmp[1].lower()) == None:
                feature.append('0')
            else:
                feature.append('1')
        feature.append(tmp[0])

        writer.writerow(feature)
    f_out.close()


if __name__=='__main__':
    main()
