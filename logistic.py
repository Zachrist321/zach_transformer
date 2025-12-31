with open("test.csv") as f:
    data = f.readlines()

data = [line.strip().split(",") for line in data]
clean = []
for row in data[1:]:
    row = [float(x) for x in row]
    clean.append(row)
print(clean[0:2])