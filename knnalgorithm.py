import operator
from csv import reader
from math import sqrt
from statistics import mode

class Flower:
    def __init__(self,
                 sepallength = 0,
                 sepalwidth = 0,
                 petallength = 0,
                 petalwidth = 0,
                 label = -1):
        self.sepallength = sepallength
        self.sepalwidth = sepalwidth
        self.petallength = petallength
        self.petalwidth = petalwidth
        self.label = label

    def __repr__(self):
        rep = str(self.sepallength) + ' | ' + str(self.sepalwidth) + ' | ' + str(self.petallength) + ' | ' + str(self.petalwidth)
        return rep
    
def create_result_file(result):
    file = open('resultados.txt', 'w')
    for i in result:
        file.write(str(int(i)) + '\n')

def get_final_results(test_results):
    file = open("rotulos-teste.txt", "r")
    results = file.readlines()
    file.close()
    for i in range(len(results)):
        results[i] = results[i][:-1]
    results.pop()
    results = [float(x) for x in results]

    matchs = 0
    for i in range(len(results)):
        if results[i] == test_results[i]:
            matchs += 1
    return (100* (matchs/len(results)))

def get_flowers_dist(f1, f2):
    dist = sqrt(
        ((f1.sepallength - f2.sepallength)**2) +
        ((f1.sepalwidth - f2.sepalwidth)**2) +
        ((f1.petallength - f2.petallength)**2) +
        ((f1.petalwidth - f2.petalwidth)**2))
    return dist


def get_flowers_data(filename):
    with open(filename, newline='') as csv:
        flowers = []
        file = reader(csv, delimiter=',')
        for row in file:
            try:
                row = [float(x) for x in row]
                flowers.append(Flower(row[0], row[1], row[2], row[3], row[4]))
            except:
                flowers.append(Flower(row[0], row[1], row[2], row[3]))            
        del flowers[0]

        return flowers

def get_neighbours(dists, k):
    nb = sorted(dists, key=operator.itemgetter(1))[0:k]
    return [x[0] for x in nb]

def get_label(neighbours):
    #since we're using mode, k must be odd
    return mode(neighbours)

trainment_flowers = get_flowers_data('treinamento.csv')
test_flowers = get_flowers_data('teste.csv')
labeled_flowers = trainment_flowers
result = []

for tested_flower in test_flowers:
    distances = []
    for lf in labeled_flowers:
        distance = get_flowers_dist(tested_flower, lf)
        distances.append([lf.label, distance])

    neighbours = get_neighbours(distances, 3)
    label = get_label(neighbours)
    tested_flower.label = label
    labeled_flowers.append(tested_flower)
    result.append(label)

create_result_file(result)
accuracy = get_final_results(result)
print('percentual de acerto: %.2f' %accuracy)
