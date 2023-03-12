import random

ranint = random.randint(1,2943)
i = 0
with open("first.txt","r") as f:
    for line in f:
        i+=1
        if i == ranint:

            fname = line.rstrip()
            print("random name: ", fname)
