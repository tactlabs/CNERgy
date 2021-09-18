f = open("data.txt" , "r")

words = f.read().split()

i=0
for word in words:
    for letter in word:
        i+=1
    