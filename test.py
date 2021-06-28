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
    sorted_fees = sorted(total_fee.items(), key=lambda x: x[1])
    #print(sorted_fees)


calculateTotalWeight()
calculateTotalFee()
parent_to_child()
sortWeights()
sortFees()
