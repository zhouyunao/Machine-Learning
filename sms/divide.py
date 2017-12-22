import os
import re
from collections import Counter
def main():
    f_in = open('sms_train.tsv','r')
    lines = []
    line = f_in.readlines()
    f_in.close()
    num_spam = 0
    num_ham = 0
    d = dict()
    word_list = list()
    phone_num_all = 0
    phone_num_spam = 0
    money_spam = 0
    money_all = 0
    mail_spam = 0
    mail_all = 0
    free_all = 0
    free_spam = 0
    http_all = 0
    http_spam = 0
    spam_count = 0
    spam_dict = list()
    ham_dict = list()
    for i in line:
        tmp = i.strip().split('\t')
        lines.append(tmp)

        if tmp[0] == 'ham':
            num_ham += 1
            for i in re.split(r'\s|\,|\.|\?|\n', tmp[1].lower()):
                ham_dict.append(i)
        else:
            num_spam += 1
            for i in re.split(r'\s|\,|\.|\?|\n', tmp[1].lower()):
                spam_dict.append(i)
            # if re.search('REPLY|reply|rply|Reply|SEND|send|Send|text|Text|Txt|txt|[0-9]{11}|pounds|CALL|call|Call|tone|TONE|Tone|£|Money|Bill|bill|buy|Buy|money|@|Free|free|FREE|http:|www.',tmp[1].lower()) == None:
            if re.search('txt|tone|[0-9]{11}|bill|£|@|free|http|www',tmp[1].lower()) == None:
                pass
            else:
                spam_count += 1


            if re.search('txt|tone|[0-9]{11}',tmp[1].lower()) == None:
                pass
            else:
                phone_num_spam += 1
            if re.search('£|bill',tmp[1].lower()) == None:
                pass
            else:
                money_spam += 1
            if re.search('@|reply|send',tmp[1]) == None:
                pass
            else:
                mail_spam += 1
            if re.search('free',tmp[1].lower()) == None:
                pass
            else:
                free_spam += 1
            if re.search('http|www.',tmp[1].lower()) == None:
                pass
            else:
                http_spam += 1

        text_tmp = tmp[1]
        words = re.split(r'\s|\,|\.|\?', text_tmp.lower())
        # text_list = text_tmp.split(' ')
        for item in words:
            if item in d:
                d[item] += 1
            else:
                d[item] = 0
            if re.match('txt|tone|[0-9]{11}',item) == None:
                pass
            else:
                phone_num_all += 1
            if re.match('£|bill',item) == None:
                pass
            else:
                money_all += 1
            if re.search('@|reply|send',item) == None:
                pass
            else:
                mail_all += 1
            if re.search('Free|free|FREE',item) == None:
                pass
            else:
                free_all += 1
            if re.search('http|www',item) == None:
                pass
            else:
                http_all += 1

            word_list.append(item)

    # print(lines)
    print ('ham:{}'.format(num_ham))
    print ('spam:{}'.format(num_spam))
    # print (d)
    print ('phone num:  ',phone_num_all,phone_num_spam)
    print ('money num: ',money_all,money_spam)
    print ('mail num: ',mail_all,mail_spam)
    print ('free num: ',free_all,free_spam)
    print ('http num: ',http_all,http_spam)
    print ('total: ',spam_count)


    ham_counter = Counter(ham_dict)
    for word, count in ham_counter.most_common(1000):
        if len(word) > 0:
            # pass
            print("%s,%d" % (word, count))
    spam_counter = Counter(spam_dict)
    for word, count in spam_counter.most_common(1000):
        if len(word) > 1:
            # pass
            print("%s,%d" % (word, count))

if __name__ == '__main__':
    main()
