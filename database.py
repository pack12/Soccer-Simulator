import sqlite3
import json
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def connect():


    con = sqlite3.connect("soccer.db")
    return con
def create_tables(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS player(playerid,first,last,overall,team)")
    cur.execute("CREATE TABLE IF NOT EXISTS teams(teamid, name,facilities,managerid,scouting,finances)")
    cur.execute("CREATE TABLE IF NOT EXISTS managers(managerid, first,last,rating, team)")

def populate_teams(con):
    cur = con.cursor()
    res = cur.execute("SELECT * FROM teams")
    # populating Teams table
    if res.fetchone() == None:
        teams_j = open("teams.json")
        teams_j = json.load(teams_j)

        for i in teams_j:
            for j in teams_j[i]:
                #print(f'{j}: {teams_j[i][j]}')
                team_id = teams_j[i][j]['teamid']
                name = j
                facilities = teams_j[i][j]['facilities']
                manager_id = None
                scouting = teams_j[i][j]['scouting']
                finances = teams_j[i][j]['finances']
                data = [(team_id, name, facilities, manager_id, scouting, finances)]
                cur.executemany("INSERT INTO teams VALUES (?,?,?,?,?,?)", data)


                manager_id = cur.execute("SELECT managers.managerid, teams.teamid "
                                         "FROM managers, teams "
                                         "WHERE teams.name = ? and managers.team = ?", (name, name))

                manager_id, team_id = manager_id.fetchone()
                #print(f'ManagerID : {manager_id} TeamID: {team_id}')

                sql_update_query = """UPDATE teams SET managerid = ? where teams.name = ? AND teams.teamid = ?"""
                data = (manager_id, name, team_id)

                cur.execute(sql_update_query, data)
def populate_players(con):
    cur = con.cursor()
    res = cur.execute("SELECT * FROM player")

    if (res.fetchone() == None):
        # Iterate through teams in order - starting with Arsenal,
        # Generate 30 players for each team
        # Ratings for the player depend on scouting, manager rating, and finances
        # Finances > scouting > manager rating

        id = 1
        for i in range(1, 21):
            sum_overall = []
            # i = teamid
            # get team name
            team = cur.execute("SELECT teams.name FROM teams WHERE teams.teamid = ?", (i,))
            team = team.fetchone()[0]
            manager_query = cur.execute("SELECT managers.rating FROM managers, teams WHERE managers.team = ?", (team,))
            manager_rating = manager_query.fetchone()[0]
            scouting_query = cur.execute("SELECT teams.scouting FROM teams WHERE teams.teamid = ?", (i,))
            scouting = scouting_query.fetchone()[0]
            finances = cur.execute("SELECT teams.finances FROM teams WHERE teams.teamid = ?", (i,))
            finances = finances.fetchone()[0]
            facilities = cur.execute("SELECT teams.facilities FROM teams WHERE teams.teamid = ?", (i,))
            facilities = facilities.fetchone()[0]
            #print(f'TEAM : {team} Manager RATING: {manager_rating} Scouting : {scouting} FINANCES: {finances} FACILITIES: {facilities}')

            for j in range(30):

                ranint = random.randint(1, 2943)
                i = 0
                with open("first.txt", "r") as f:
                    for line in f:
                        i += 1
                        if i == ranint:
                            fname = line.rstrip()

                ranint = random.randint(1, 2000)
                i = 0
                with open("last.txt", "r") as l:
                    for line in l:
                        i += 1
                        if i == ranint:
                            lname = line.rstrip()
                # Get finance rating, scouting rating and manager rating
                # Formula = 1 * (99 * finance) + (99 * scouting) + (99 * manager rating)

                overall = round(1.3 * (((99 * (int(finances) * 0.47)) / 100) + ((99 * (int(scouting) * 0.28)) / 100) + (
                            (99 * (int(manager_rating) * 0.25)) / 100)))

                if overall > 95:
                    std = random.randint(-10, -facilities)
                else:
                    std = random.randint(0 - facilities, facilities)
                if overall + std > 100:
                    pass
                else:

                    overall += std
                sum_overall.append(overall)

                data = [(id, fname, lname, overall, team)]

                cur.executemany("INSERT INTO player VALUES(?,?,?,?,?)", data)
                id += 1
            print(f'Team: {team} Sum rating: {sum(sum_overall)}')

def populate_managers(con):
    cur = con.cursor()

    res = cur.execute("SELECT * FROM managers")
    # Populating Manager table
    if res.fetchone() == None:
        i = 1
        m = open("managers.txt", "r")
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
                data = [(i, fname, lname, rating, team)]
                cur.executemany("INSERT INTO managers VALUES(?,?,?,?,?)", data)
                i += 1

def drop_tables(con):
    cur = con.cursor()

    #For testing purposes
    cur.execute("DROP TABLE player")
    cur.execute("DROP TABLE teams")
    cur.execute("DROP TABLE managers")

def execute_user_command(con, usr_input):
    cur = con.cursor()
    try:


        res = cur.execute(usr_input)

    except:
        print("Invalid SQL Command! Try again")
    else:
        for i in res.fetchall():

            print(i)