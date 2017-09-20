#knn.py
#
#Felipe Ferreira
#9/13/17

import random
import sys
import collections
import statistics

def confusionmatrix(predictions, all_labels):
    matrix = []
    matrix.append(all_labels)
    for x in all_labels:
        addrow = []
        for y in all_labels:
            addrow.append(0)
        for z in all_labels:
            for i in predictions[z]:
                if i[0] == x:
                    addrow[all_labels.index(z)] += 1
        addrow.append(x)
        matrix.append(addrow)
    return matrix

def predict(knearv):
    prediction = []
    prediction1 = []
    #print(knearv)
    for x in range(0, len(knearv)):
        prediction.append(max(knearv[x], key = knearv.count))
    prediction1.append(max(prediction, key = prediction1.count))
    #print(prediction1)
    return prediction1

def predict2(knearv):
    prediction = []
    prediction1 = []
    #print(knearv)
    for x in range(0, len(knearv)):
        prediction.append(max(knearv[x], key = knearv.count))
    prediction1.append(max(prediction, key = prediction1.count))
    #print(prediction1)
    return prediction1

def findk(testset, trainingset, x):
    knear = {}
    for y in range(0, len(trainingset)):
        math = []
        q = 0
        for z in range(1, len(testset[3])):
            i = float(testset[x][z]) - float(trainingset[y][z])
            math.append(i**2)
        for t in range(0,len(math)):
            q = q + math[t]
        q = q**(1/2)
        knear[q] = trainingset[y]
    knear = collections.OrderedDict(sorted(knear.items()))
    #print(knear)
    return knear

def findk2(testset, trainingset, x):
    knear = {}
    for y in range(0, len(trainingset)):
        math = []
        q = 0
        for z in range(1, len(testset[3])):
            if(testset[x][z] == trainingset[y][z]):
                math.append(int(1))
            else:
                math.append(int(0))
        for t in range(0, len(math)):
            q = q + math[t]
        if not q in knear.keys():
            knear[q] = [(trainingset[y])]
        else:
            knear[q].append((trainingset[y]))
        #print(knear[q])
    #knear = collections.OrderedDict(sorted(knear.items()))
    #print(knear)
    return knear

def euclidian(testset, trainingset, k):
    knear1k = []
    knear1v = []
    predictions = {}
    for x in range(0, len(testset)):
        knearest = findk(testset, trainingset, x)
        kneark = []
        knearv = []
        for u in range(0, k):
            kneark.append(list(knearest.keys())[u])
            knearv.append(list(knearest.values())[u])
        knear1k.append(kneark)
        prediction = predict(knearv)
        if prediction[0] in predictions.keys():
            predictions[prediction[0]].append((testset[x]))
        else:
            predictions[prediction[0]] = [(testset[x])]
        knear1v.append(knearv)
    return predictions

def hamming(testset, trainingset, k):
    knear1k = []
    knear1v = []
    predictions = {}
    for x in range(0, len(testset)):
        knearest = findk2(testset, trainingset, x)
        kneark = []
        knearv = []
        count = len(knearest) - 1
        lists = list(reversed(sorted(knearest.keys())))
        #print(lists)
        v = 0
        for u in range(0,k):
            #kneark.append(list(knearest.keys())[u])
            try:
                knearv.append(list(knearest[lists[v]])[u])
                break
            except IndexError:
                v = v + 1
                knearest.append(list(knearest[lists[v]])[u])
        #knear1k.append(kneark)
        #print(knearv)
        prediction = predict2(knearv)
        if prediction[0] in predictions.keys():
            predictions[prediction[0]].append((testset[x]))
        else:
            predictions[prediction[0]] = [(testset[x])]
        knear1v.append(knearv)
        #print(prediction)
    return predictions
    

def findtest(instances, index):
    testset = []
    count = 0
    for x in range(index, len(instances)):
        testset.append(instances[x])
        count = count + 1
    #print(count)
    return testset

def findtrain(instances, index):
    trainingset = []
    counter = 0
    for x in range(0, index):
        trainingset.append(instances[x])
        counter = counter + 1
    #print(counter)
    return trainingset

def main():
    filename = sys.argv[1]
    distfunc = sys.argv[2]
    valofk = int(sys.argv[3])
    percent = float(sys.argv[4])
    randseed = sys.argv[5]

    file = open(filename, "r")
    labels = file.readline()
    labels = labels.replace("\n", "")
    label = labels.split(",")

    instances = []
    for line in file:
        line = line.replace("\n", "")
        instance = line.split(",")
        instances.append(instance)

    #print(instances)
     
    all_labels = []
    for i in range(0, len(instances)):
        if instances[i][0] not in all_labels:
            all_labels.append(instances[i][0])
            
    random.seed(randseed)
    random.shuffle(instances)
    #print(len(instances))
    index = int((len(instances) * (100 * percent)) // 100)
    #^finds index of instances at percentage passed in by argv

    trainingset = findtrain(instances, index)
    testset = findtest(instances, index)

    #few print debugging
    #print(index)
    #print(instances)
    #print(trainingset)
    #print(testset)

    if(distfunc == 'E'):
        prediction = euclidian(testset, trainingset, valofk)
    elif(distfunc == 'H'):
        prediction = hamming(testset, trainingset, valofk)
    else:
        print("Error: Invalid Distance Function")

    #print(prediction.items())
    matrix = confusionmatrix(prediction, all_labels)
    export = open("export.txt", "w")
    firsttime = 0
    for row in matrix:
        for word in row:
            export.write(str(word))
            if(word != row[-1]) or (firsttime < 1):
                export.write(",")
        firsttime += 1
        export.write('\n')
    export.close()
    
main()
