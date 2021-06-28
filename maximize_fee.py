import csv
from collections import OrderedDict

included = OrderedDict()        #keeps track of which transaction is included in block
fee = OrderedDict()        #fee of all transaction
weight = OrderedDict()        #weight of all transactions
total_fee = OrderedDict()        #contains parent transaction fee + child transaction fee
total_weight = OrderedDict()        #contains parent transaction weight + child transaction weight
parents = OrderedDict()        #maps child transactions to parent transactions
child = OrderedDict()        #maps parent transactions to child transactions
current_fee = 0        #keeps track of cumulative fee
current_weight = 0        #keeps track of cumulative weight
block_weight = 4000000        #maximum block weight
no_of_txid = 0        #number of transactions

File_object = open("block.txt","w+")

with open('mempool.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        included[row[0]] = False
        fee[row[0]] = int(row[1])
        weight[row[0]] = int(row[2])
        total_fee[row[0]] = int(row[1])
        total_weight[row[0]] = int(row[2])
        parents[row[0]] = row[3].split(";")
        line_count += 1
    print(f'Processed {line_count} lines.')
    no_of_txid = line_count

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

def isChild(txid):
    for j in parents[txid]:
        if j == '':
            return False
    return True

def isParent(txid):
    return True if txid in child else False

def includeTransaction(txid):
    global current_weight, current_fee
    if (included[txid] == False):
        if (current_weight + weight[txid] <= block_weight):
            current_weight += weight[txid]
            current_fee += fee[txid]
            included[txid] = True
            File_object.write(txid + '\n')

def includeParent(txid):
    if (isChild(txid) == False):
        includeTransaction(txid)
    else :
        for i in parents[txid]:
            includeParent(i)
    includeTransaction(txid)

def selectTransactions():
    global current_fee, current_weight
    sorted_fees = sorted(total_fee.items(), key=lambda x: x[1], reverse = True)
    for i in sorted_fees:
        txid = i[0]
        if (isChild(txid)):
            if (current_weight + total_weight[txid] <= block_weight):
                includeParent(txid)
        else:
            if (current_weight + weight[txid] <= block_weight):
                includeTransaction(txid)


calculateTotalWeight()
calculateTotalFee()
parent_to_child()
selectTransactions()
File_object.close()

print(current_fee, " ", current_weight)