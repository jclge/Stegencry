import random
import copy

SEED = 99999999999

myList = [[1, 2, 3, 4, 123, 2], [5, 6, 7, 8, 123, 3], [9, 10, 11, 12, 123, 4], [13, 14, 15, 16, 123, 5], [17, 18, 19, 20, 123, 6]]
random.seed(SEED)
random.shuffle(myList)
i = 0
while (i != (len(myList))):
    tmp = myList[i]
    random.seed(SEED)
    random.shuffle(tmp)
    myList[i] = tmp
    i+=1

random.seed(SEED)
Order = list(range(len(myList)))
random.shuffle(Order)
random.seed(SEED)
subOrder = list(range(len(myList[0])))
random.shuffle(subOrder)
i = 0
new = []
for element in myList:
    new.append(copy.deepcopy(element))
for element in myList:
    new[Order[i]] = copy.deepcopy(myList[i])
    tmp = copy.deepcopy(new[Order[i]])
    j = 0
    for subelem in new[Order[i]]:
        tmp[subOrder[j]] = copy.deepcopy(subelem)
        j+=1
    new[Order[i]] = copy.deepcopy(tmp)
    i+=1
print(new)