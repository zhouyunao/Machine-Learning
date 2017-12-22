import os
import re
import csv



# IP feature
def IP_feature(addr):
    addr = list(map(int,addr.split('.')))
    ip_feature_v = [0 for i in range(768)]
    for n in range(len(addr-1)):
        index = 2**8*n + addr[n]
        ip_feature_v[index] = 1
        return ip_feature_v



def main():
    f_out = open('trained.csv','w')
    writer = csv.writer(f_out,lineterminator='\n')
    f_in = open('net_train.csv','r')
    reader = csv.reader(f_in)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        print(row)
        feature = IP_feature(row[1])
        if row[0] == 'spam':
            feature = feature.append(0)
        else:
            feature = feature.append(1)
        writer.writerow(feature)

    f_out.close()
    f_in.close()


if __name__=='__main__':
    main()
