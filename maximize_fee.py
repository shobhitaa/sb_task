import csv
from collections import OrderedDict

included = OrderedDict()        #keeps track of which transaction is included in block
fee = OrderedDict()        #fee of all transaction
weight = OrderedDict()        #weight of all transactions
total_fee = OrderedDict()        #contains parent transaction fee + child transaction fee
total_weight = OrderedDict()        #contains parent transaction weight + child transaction weight
parents = OrderedDict()        #maps child transactions to parent transactions
child = OrderedDict()        #maps parent transactions to child transactions
cumulative_fee = 0        #keeps track of cumulative fee
cumulative_weight = 0        #keeps track of cumulative weight
block_weight = 4000000        #maximum block weight
no_of_txid = 0        #number of transactions

File_object = open("block.txt","w+")

#reading input from csv file
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
    no_of_txid = line_count

def calculateWeight() -> None:
    '''add weight of parent transactions to weight of child transactions'''
    for i in total_weight:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                total_weight[i] += total_weight[j]

def calculateFee() -> None:
    '''add fee of parent transactions to fee of child transactions'''
    for i in total_fee:
        for j in parents[i]:
            if(j == ''):
                continue
            else:
                total_fee[i] += total_fee[j]

def parentToChild() -> None:
    '''create 'child' dictionary to map parent transaction to child transaction'''
    for i in parents:
        for j in parents[i]:
            if j == '':
                continue
            else:
                child[j] = []
                child[j].append(i)

def isChild(txid: str) -> bool:
    '''returns True if a transaction has parent transactions'''
    for j in parents[txid]:
        if j == '':
            return False
    return True

def isParent(txid: str) -> bool:
    '''returns True if a transaction has child transactions'''
    return True if txid in child else False

def includeTransaction(txid: str) -> None:
    '''includes transaction in the block'''
    global cumulative_weight, cumulative_fee
    if (included[txid] == False):
        if (cumulative_weight + weight[txid] <= block_weight):
            cumulative_weight += weight[txid]
            cumulative_fee += fee[txid]
            included[txid] = True
            File_object.write(txid + '\n')

def includeParent(txid: str) -> None:
    '''finds and includes parent transactions to the block of a child transaction'''
    if (isChild(txid) == False):
        includeTransaction(txid)
    else :
        for i in parents[txid]:
            includeParent(i)
    includeTransaction(txid)

def selectTransactions():
    '''selects transactions with the highest fees'''
    global cumulative_fee, cumulative_weight
    #sort transactions accourding to fee in desending order
    sorted_fees = sorted(total_fee.items(), key=lambda x: x[1], reverse = True)
    for i in sorted_fees:
        txid = i[0]
        if (isChild(txid)):        #if transaction has parent transactions
            if (cumulative_weight + total_weight[txid] <= block_weight):
                includeParent(txid)
        else:        #if transaction does not have any parent transactions
            if (cumulative_weight + weight[txid] <= block_weight):
                includeTransaction(txid)


calculateWeight()
calculateFee()
parentToChild()
selectTransactions()
File_object.close()

print("Total Fee = ", cumulative_fee, " ", "Total weight = ", cumulative_weight)