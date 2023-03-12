import sqlite3
import random
con = sqlite3.connect("soccer.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS player(first,last,overall,team)")
res = cur.execute("SELECT * FROM player")
if(res.fetchone() == None):
    print("this executed")


    for i in range(11):
        ranint = random.randint(1, 2943)
        i = 0
        with open("first.txt", "r") as f:
            for line in f:
                i += 1
                if i == ranint:
                    fname = line.rstrip()

        ranint = random.randint(1,2000)
        i = 0
        with open("last.txt", "r") as l:
            for line in l:
                i+=1
                if i == ranint:

                    lname = line.rstrip()
        rand_overall = random.randint(1,99)
        data = [(fname,lname,rand_overall,"Liverpool")]
        cur.executemany("INSERT INTO player VALUES(?,?,?,?)",data)
        con.commit()
    for i in range(11):
        ranint = random.randint(1, 2943)
        i = 0
        with open("first.txt", "r") as f:
            for line in f:
                i += 1
                if i == ranint:
                    fname = line.rstrip()

        ranint = random.randint(1,2000)
        i = 0
        with open("last.txt", "r") as l:
            for line in l:
                i+=1
                if i == ranint:

                    lname = line.rstrip()
        rand_overall = random.randint(1,99)
        data = [(fname,lname,rand_overall,"Arsenal")]
        cur.executemany("INSERT INTO player VALUES(?,?,?,?)",data)
        con.commit()



res = cur.execute("SELECT * FROM player")
for i in (res.fetchall()):
    print(i[0], i[1], i[2],i[3])
#print(res.fetchall())
cur.execute("DROP TABLE player")

#Steps for this 'program'

#INSERT,UPDATE,DELETE,REPLACE are execute statements
"""
In order to do this I need to have a text file full of all different first names
and different text file of last names

1. Create table called player
2. Populate table with random players on different teams
3. """


