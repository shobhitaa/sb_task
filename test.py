import csv
from collections import OrderedDict

fee = OrderedDict()
weight = OrderedDict()
parents = OrderedDict()
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
        parents[row[0]] = row[3].split(";")
        line_count += 1
    print(f'Processed {line_count} lines.')
    no_of_txid = line_count

#matrix = [[0 for x in range(0, block_weight + 1)] for x in range(0, no_of_txid + 1)]

def calculateTotalWeight():
    for i in weight:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                weight[i] += weight[j]

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

def dp():
    temp_list = []
    temp_list2 = []
    sorted_weights = sorted(weight.items(), key=lambda x: x[1])
    for i in range(0, block_weight + 1):
        temp_list.append(0)
    matrix.append(temp_list)

    for i in range(1, no_of_txid + 1):
        txid = sorted_weights[i - 1][0]
        for j in range(0, 4000000 + 1):
            str1 = 'matrix[' + txid + "][" + str(j) + "]"
            if j == 0:
                temp_list2.append(0)
            elif sorted_weights[i - 1][1] < j:
                # print(fee[txid])
                value = max(fee[txid] + matrix[i - 1][j - sorted_weights[i - 1][1]], matrix[i - 1][j])
                temp_list2.append(value)
            else:
                value = matrix[i - 1][j]
                temp_list2.append(value)
            matrix_map[str1] = []
        matrix.append(temp_list2)
        #print(matrix)

            


calculateTotalWeight()
sortWeights()
dp()

