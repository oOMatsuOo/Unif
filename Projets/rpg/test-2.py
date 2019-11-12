import csv

with open("maps/map_1/maps.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    liste = list(csv_reader)
    print(len(liste[1]))
    print(len(liste))
    for row in csv_reader:
        #print('...'.join(row))
        #print(csv_reader.__next__())
        line_count +=1
    print(line_count)