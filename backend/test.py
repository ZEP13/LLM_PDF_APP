fruits =["pomme", "banane", "pomme"]

freq =[[] for i in range(len(fruits))]

count = {}
for i in fruits:
    count[i]= 1 + count.get(i, 0)

for n, c in count.items():
    freq[c].append(n)


print(count)
print(freq)