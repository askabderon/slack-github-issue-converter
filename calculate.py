dict1 = {}
dict2 = {}

f = open("first.txt", "r")
Lines = f.readlines()

for line in Lines:
  line2 = line.strip().split()
  dict1[line2[0]]=line2[1]
f.close()

f = open("second.txt", "r")
Lines = f.readlines()

for line in Lines:
  line2 = line.strip().split()
  dict2[line2[0]]=line2[1]
f.close()

diff1 = []

ind = 0

while ind<100:
  c = str(ind + int('0'))
  if(c in dict1 and c in dict2 ):
    diff1.append(float(dict2[c])-float(dict1[c]))
  ind+=1

print(diff1)
n1 = len(diff1)
mean1 = sum(diff1) / n1
deviations1 = [(x - mean1) ** 2 for x in diff1]
variance1 = sum(deviations1) / n1
print(mean1, variance1)
