import csv



with open("maps.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        character_count = 0
        while character_count < 7:
            print(f"{row[character_count]}", end=' ')
            character_count += 1
        line_count += 1
        print()
    print(f"Processed {line_count} lines")
    