import os
import math
import csv
import re
#--------------input-----------------
def data_input():
    f_in = open('train.csv','r')
    lines = []
    line = f_in.readlines()
    f_in.close()
    for i in line:
        lines.append(i.strip().split(','))

    # print(lines)
    return lines
class NBC():
    def __init__(self,data):
        self.dataset = data
        self.Pr_spam = 0
        self.Pr_ham = 0
        self.Pr_spam_lh_1 = []
        self.Pr_ham_lh_1 = []
        self.Pr_spam_lh_0 = []
        self.Pr_ham_lh_0 = []
#-------------laplace-----------------
    def laplace_c(self,n,n_i,n_ij):
        P = (n_ij+0.1)/(n+0.1*n_i)
        return P

#--------------traning--------------
    def training(self):
        num_all = len(self.dataset)
        num_spam = 0
        num_ham = 0
        # num_spam_1 = [0]*len(self.dataset[0]-1)
        # これは絶対ダメ
        num_spam_1 = [0 for i in range(len(self.dataset[0])-1)]
        num_ham_1 = [0 for j in range(len(self.dataset[0])-1)]
        num_spam_0 = [0 for i in range(len(self.dataset[0])-1)]
        num_ham_0 = [0 for j in range(len(self.dataset[0])-1)]


        for item in self.dataset:
            if item[-1] == 'spam':
                num_spam += 1
                for i in range(len(item)-1):
                    if item[i] == '1':
                        num_spam_1[i] += 1
                    else:
                        num_spam_0[i] += 1
            else:
                num_ham += 1
                for i in range(len(item)-1):
                    if item[i] == '1':
                        num_ham_1[i] += 1
                    else:
                        num_ham_0[i] += 1

        # Pr[Xi=j|C=0] = (# of spam messages with feature Xi=j)/# of spam messages
        for i in range(len(num_spam_1)):
            tmp_Pr = num_spam_1[i]/num_spam
            if tmp_Pr == 0:
                tmp_Pr = self.laplace_c(num_spam,num_spam_1[i]+num_ham_1[i],num_spam_1[i])
            self.Pr_spam_lh_1.append(tmp_Pr)


        for i in range(len(num_spam_0)):
            tmp_Pr = num_spam_0[i]/num_spam
            if tmp_Pr == 0:
                tmp_Pr = self.laplace_c(num_spam,num_spam_0[i]+num_ham_0[i],num_spam_0[i])
            self.Pr_spam_lh_0.append(tmp_Pr)


        for i in range(len(num_ham_1)):
            tmp_Pr = num_ham_1[i]/num_ham
            if tmp_Pr == 0:
                tmp_Pr = self.laplace_c(num_ham,num_ham_1[i]+num_spam_1[i],num_ham_1[i])
            self.Pr_ham_lh_1.append(tmp_Pr)


        for i in range(len(num_ham_0)):
            tmp_Pr = num_ham_0[i]/num_ham
            if tmp_Pr == 0:
                tmp_Pr = self.laplace_c(num_ham,num_ham_0[i]+num_spam_0[i],num_ham_0[i])
            self.Pr_ham_lh_0.append(tmp_Pr)
        # for i in num_ham_1:
        #     tmp_Pr = i/num_ham
        #     self.Pr_ham_lh_1.append(tmp_Pr)
        #
        # for i in num_spam_0:
        #     tmp_Pr = i/num_spam
        #     self.Pr_spam_lh_0.append(tmp_Pr)
        #
        # for i in num_ham_0:
        #     tmp_Pr = i/num_ham
        #     self.Pr_ham_lh_0.append(tmp_Pr)

        self.Pr_spam = num_spam/num_all
        self.Pr_ham = 1-self.Pr_spam

        print ('Pr_spam:{}'.format(self.Pr_spam))
        print ('spam feature 1 likehood:{}'.format(self.Pr_spam_lh_1))
        print ('ham feature 1 likehood:{}'.format(self.Pr_ham_lh_1))
        print ('spam feature 0 likehood:{}'.format(self.Pr_spam_lh_0))
        print ('ham feature 0 likehood:{}'.format(self.Pr_ham_lh_0))


#-------------classify--------------
    def classify(self,addr):
        # Pr_Numerator = 1 #分母
        # Pr_Denominator = 1 #分子
        addr = addr.strip().split(',')
        w = 0
        b = math.log2(self.Pr_spam) - math.log2(self.Pr_ham)
        # for (i,j) in zip(self.Pr_spam_lh_1,self.Pr_ham_lh_1):
        #     tmp_w = math.log2(i) - math.log2(j)
        #     w *= tmp_w
        for i in range(len(addr)):
            if addr[i] == '1':
                tmp_w = math.log2(self.Pr_spam_lh_1[i])-math.log2(self.Pr_ham_lh_1[i])
                w += tmp_w
                # print ('1')
            else:
                tmp_w = math.log2(self.Pr_spam_lh_0[i])-math.log2(self.Pr_ham_lh_0[i])
                w += tmp_w
        p = 1/(1+math.exp(-w-b))
        try:
            ans = p/(1-p)
        except ZeroDivisionError:
            return 999
        # print ('the result is : {}'.format(ans))
        # print ('p:{}'.format(p))
        return ans






def main():
    re_spam = 0
    re_all = 0
    f_out = open('result.csv','w')

    writer = csv.writer(f_out,lineterminator='\n')
    # stock = 'reply|send|text|txt|[0-9]{11}|pound|call|tone|£|money|bill|buy|money|@|free|http|www'
    # stock = stock.split('|')
    data = data_input()
    test = NBC(data)
    test.training()

    f1 = open('stock.csv','r')
    stock = f1.readline().strip().split(',')
    f1.close()
    print (stock)

    f = open('sms_test.tsv','r')
    lines = f.readlines()
    f.close()
    for l in lines:
        tmp = l.split('\t')
        feature = []
        for c in stock:
            if re.search(c,tmp[1].lower()) == None:
                feature.append('0')
            else:
                feature.append('1')
        if test.classify(','.join(feature))>=1:
            writer.writerow([tmp[0],'spam'])
            re_spam += 1
        else:
            writer.writerow([tmp[0],'ham'])
        re_all += 1
    f_out.close()
    print (re_spam)
    print (re_all)

if __name__=='__main__':
    main()
