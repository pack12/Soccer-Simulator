import json
import sqlite3
import random
con = sqlite3.connect("soccer.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS player(playerid,first,last,overall,team)")
cur.execute("CREATE TABLE IF NOT EXISTS teams(teamid, name,facilities,managerid,scouting)")
cur.execute("CREATE TABLE IF NOT EXISTS managers(managerid, first,last,rating, team)")

#res = cur.execute("SELECT name FROM teams WHERE name='Arsenal'")

res = cur.execute("SELECT * FROM managers")
#Populating Manager table
if res.fetchone() == None:
    i=1
    m = open("managers.txt","r")
    with open("teams.txt", "r") as f:
        for line in f:
            line = line.rstrip()
            team_arr = line.split("-")
            team = team_arr[0]
            name = team_arr[1]
            name_arr = name.split(" ")
            fname = name_arr[0]
            lname = name_arr[1]
            lm = m.readline()
            lm = lm.rstrip()
            manager_arr = lm.split("-")
            rating = manager_arr[1]
            data = [(i,fname,lname,rating,team)]
            cur.executemany("INSERT INTO managers VALUES(?,?,?,?,?)", data)
            i+=1


print("excute select * FROM managers: ")
res = cur.execute("SELECT * FROM managers")
for i in res.fetchall():
    print(i[0],i[1],i[2],i[3])

if res.fetchone() == None:

    for i in range(20):

        with open("teams.txt","r") as f:
            for line in f:
                line = line.rstrip()
                team_arr = line.split("-")
                team = team_arr[0]
                manager = team_arr[1]


                man_arr = manager.split(" ")
                first = man_arr[0]
                last = man_arr[1]



                #print(team_arr[0])
                #print(team_arr[1])

#store result of sql statement into res
res = cur.execute("SELECT * FROM player")



#Populating the player table
if(res.fetchone() == None):


    id = 1
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
        rand_overall = random.randint(70,int(99*0.9))

        data = [(id,fname,lname,rand_overall,"Liverpool")]
        cur.executemany("INSERT INTO player VALUES(?,?,?,?,?)",data)
        con.commit()
        id +=1
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

        rand_overall = random.randint(65,int(99*0.9))
        data = [(id,fname,lname,rand_overall,"Arsenal")]
        cur.executemany("INSERT INTO player VALUES(?,?,?,?,?)",data)
        con.commit()
        id+=1

res = cur.execute("SELECT * FROM teams")
#populating Teams table
if res.fetchone() == None:
    teams_j = open("teams.json")
    teams_j = json.load(teams_j)

    for i in teams_j:
        for j in teams_j[i]:
            print(f'{j}: {teams_j[i][j]}')
            team_id = teams_j[i][j]['teamid']
            name = j
            facilities = teams_j[i][j]['facilities']
            manager_id = None
            scouting = teams_j[i][j]['scouting']
            data = [(team_id, name, facilities, manager_id, scouting)]
            cur.executemany("INSERT INTO teams VALUES (?,?,?,?,?)", data)

            #manager_id = cur.execute("SELECT managers.managerid FROM managers, teams WHERE teams.name = 'Arsenal' and managers.team = 'Arsenal'")
            manager_id = cur.execute("SELECT managers.managerid "
                                     "FROM managers, teams "
                                     "WHERE teams.name = ? and managers.team = ?", (name, name))
            print("THIS IS OUR MANAGER_ID FROM SQL execution: ", manager_id.fetchone(), "should be: ", name)

            #We need to find the manager id based off of team?
            # select managers.id
            #from managers, teams
            #where teams.name = managers.team




print(res.fetchall())
res = cur.execute("SELECT * FROM player")
for i in (res.fetchall()):
    print(i[0], i[1], i[2],i[3],i[4])


ratings_team_a = []
ratings_team_b = []
for i in cur.execute("SELECT player.overall, player.first, player.last, player.team FROM player ORDER BY overall"):
    print("Rating: ",i[0],i[1],i[2],"Team: ",i[3])

    if i[3] == "Arsenal":

        ratings_team_a.append(i[0])
    else:
        ratings_team_b.append(i[0])

print("Arsenal total Rating: ", sum(ratings_team_a))
print("Liverpool total Rating: ", sum(ratings_team_b))


man = cur.execute("SELECT managers.rating, managers.managerid, managers.team from managers")
for i in man.fetchall():
    print("Manager Rating: ", i[0],"ID: ",i[1], "Team: ", i[2])

man = cur.execute("SELECT managers.rating, managers.managerid, teams.managerid, managers.first, managers.last, teams.name "
                  "FROM managers,teams "
                  "WHERE managers.team = teams.name")

print(man.fetchall())
cur.execute("DROP TABLE player")
cur.execute("DROP TABLE teams")
cur.execute("DROP TABLE managers")

#INSERT,UPDATE,DELETE,REPLACE are execute statements



