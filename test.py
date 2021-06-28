import csv
from collections import OrderedDict

fee = OrderedDict()
weight = OrderedDict()
total_fee = OrderedDict()
total_weight = OrderedDict()
parents = OrderedDict()
child = OrderedDict()
matrix_map = OrderedDict()
matrix_dictionary = OrderedDict()
sorted_weights = []
block_weight = 4000000
no_of_txid = 0
matrix =[]
File_object = open("block.txt","w+")

with open('mempool.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        #print(f'\t fee = {row[1]} , weight {row[2]} , ptid = {row[3]}')
        fee[row[0]] = int(row[1])
        weight[row[0]] = int(row[2])
        total_fee[row[0]] = int(row[1])
        total_weight[row[0]] = int(row[2])
        parents[row[0]] = row[3].split(";")
        line_count += 1
    print(f'Processed {line_count} lines.')
    no_of_txid = line_count

#matrix = [[0 for x in range(0, block_weight + 1)] for x in range(0, no_of_txid + 1)]

def calculateTotalWeight():
    for i in total_weight:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                total_weight[i] += total_weight[j]

def calculateTotalFee():
    for i in total_fee:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                total_fee[i] += total_fee[j]

def parent_to_child():
    for i in parents:
        for j in parents[i]:
            if j == '':
                continue
            else:
                child[j] = []
                child[j].append(i)


def sortWeights():
    sorted_weights = sorted(weight.items(), key=lambda x: x[1])
    #j = 1
    #print(sorted_weights[0][1])
    # for i in list(sorted_weights.keys()):
    #     sorted_ids[i] = j
    #     j += 1
    # print(sorted_ids)
    # c = 1
    # for i in sorted_weights:
    #     print(c, i[0], i[1])
    #     c = c + 1

def sortFees():
    return sorted(total_fee.items(), key=lambda x: x[1], reverse = True)
    # c = 1
    # for i in sorted_fees:
    #     print(c, " " ,i[0], " ", i[1])
    #     c += 1

def isChild(txid):
    for j in parents[txid]:
        if j == '':
            return False
    return True

def isParent(txid):
    if txid in child:
        return True
    else:
        return False

def removeFee(txid, parent_fee):
    for i in child[txid]:
        total_fee[i] -= parent_fee

def selectTransactions():
    sorted_fees = sortFees()
    current_weight = 0
    current_fee = 0
    for i in sorted_fees:
        txid = i[0]
        
        if (isChild(txid)):
            continue
        else:
            # print(txid)
            # print(weight[txid])
            if (current_weight + weight[txid] <= 9000):
                current_weight += weight[txid]
                current_fee += fee[txid]
                File_object.write(txid + '\n')
            else:
                break
    print(current_fee)


calculateTotalWeight()
calculateTotalFee()
parent_to_child()
sortWeights()
sortFees()

# sorted_fees = sorted(total_fee.items(), key=lambda x: x[1])
# print(weight[sorted_fees[5213][0]])
selectTransactions()
# print(isChild('59f0495cf66d1864359dda816eb7189b9d9a3a9cd9dc50a3707776b41a6c815b'))
File_object.close()