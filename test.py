import csv
from collections import OrderedDict

fee = OrderedDict()
weight = OrderedDict()
parents = OrderedDict()
matrix_dictionary = OrderedDict()

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

def calculateTotalWeight():
    for i in weight:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                weight[i] += weight[j]

def sortWeights():
    sorted_weights = sorted(weight.items(), key=lambda x: x[1])
    # c = 1
    # for i in sorted_weights:
    #     print(c, i[0], i[1])
    #     c = c + 1


calculateTotalWeight()
sortWeights()

