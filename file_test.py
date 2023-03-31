import random


i = 0
m = open("managers.txt","r")
with open("teams.txt","r") as f:
    for line in f:
        line = line.rstrip()
        team_arr = line.split("-")

        team = team_arr[0]
        name = team_arr[1]
        name_arr = name.split(" ")
        fname = name_arr[0]
        lname = name_arr[1]
        #print(team_arr[0])
        #print(team_arr[1])

        lm = m.readline()
        lm = lm.rstrip()
        #print(lm)
        manager_arr = lm.split("-")
        rating = manager_arr[1]
        print(f'Manager Name: {fname} {lname}|rating:{rating}|team: {team}')