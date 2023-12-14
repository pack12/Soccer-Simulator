import sqlite3
import json
import random
import match
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

"""Create connection object to soccer.db"""
def connect():


    con = sqlite3.connect("soccer.db")
    return con

"""Create datatables"""
def create_tables(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS player(playerid,first,last,overall,team)")
    cur.execute("CREATE TABLE IF NOT EXISTS teams(teamid, name,facilities,managerid,scouting,finances)")
    cur.execute("CREATE TABLE IF NOT EXISTS managers(managerid, first,last,rating, team)")
    cur.execute("CREATE TABLE IF NOT EXISTS schedule(teamid, week_1, week_2, week_3, week_4, week_5, week_6, week_7, week_8, week_9,"
                "week_10, week_11, week_12, week_13, week_14, week_15, week_16, week_17, week_18, week_19, week_20, week_21,"
                "week_22, week_23, week_24, week_25, week_26, week_27, week_28, week_29, week_30, week_31, week_32, week_33, "
                "week_34, week_35, week_36, week_37, week_38)")
    #cur.execute("CREATE TABLE IF NOT EXISTS player_attributes(playerid,)")

"""Use Json to create Teams datatable"""
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
            # print(f'Team: {team} Sum rating: {sum(sum_overall)}')

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
    cur.execute("DROP TABLE schedule")

"""Functionality of executing sqlite command line"""
def execute_user_command(con, usr_input):
    cur = con.cursor()
    try:


        res = cur.execute(usr_input)

    except:
        print("Invalid SQL Command! Try again")
    else:
        for i in res.fetchall():

            print(i)

"""Helper function to get team info"""
def get_team_info(con,team):
    cur = con.cursor()
    team_info = cur.execute("select * from teams where teams.name = ?",(team,))
    return team_info
    # for i in team_info.fetchall():
    #     print(i[0])


def generate_schedule(con):

    cur = con.cursor()
    teams = cur.execute("select teams.name from teams")
    # teams = teams.fetchall()
    rnd = random.randint(0, 19)

    #Prints Teams: <sqlite3.Cursor object
    print(f'Teams: {teams}')


    lst_team = []
    for i in teams.fetchall():
        # print(i[0])
        """Add names of team to lst_team"""
        lst_team.append(i[0])

    original_teams = lst_team
    print(f'Original 1: {original_teams}')




    """My assumption is that this part of the code is used to use original list and create a schedule"""
    for i in range(len(original_teams)):
        home_team = original_teams[i]
        low = 0
        week = 1
        team_id = get_team_info(con, home_team)
        team_id = team_id.fetchone()[0]
        # print(f'Teaminfo: {team_id}')

        """Double the list, so it goes Arsenal...Wolves, Arsenal ... Wolves"""
        lst_team = original_teams * 2

        for j in range(len(lst_team)):

            rnd = random.randint(low,len(lst_team)-1)
            # print(f'Rand: {rnd}')
            temp = lst_team[rnd]

            #Swap teams with random index
            lst_team[rnd] = lst_team[j]
            lst_team[j] = temp


            """My assumption is that this part is to prevent teams playing back-to-back
            so Arsenal can't play Crystal Palace Week 18, and then play Crystal Palace Week 19"""
            if j+1 < 39 and lst_team[j] == lst_team[j+1]:
                # print("When does this execute?")


                # Do another swap
                rnd = random.randint(low, 39)

                # swap teams with random index
                temp = lst_team[rnd]
                lst_team[rnd] = lst_team[i]
                lst_team[i] = temp

            if week == 39:
                week -= 1
            insert_into_schedule(con,team_id,week,lst_team[j])
            scheddd = cur.execute("select * from schedule")
            for row in scheddd.fetchall():
                print(f'ROW: {row}')
            week+=1

            low+=1

        for k in range(2):
            if home_team in lst_team:
                lst_team.remove(home_team)
        print(f'{home_team} -Iteration {i} {lst_team}')





"""Inserts teamid values into schedule datatable"""
def generate_initial_schedule_value(cursor):
    cur = cursor
    #Generate all of the team_ids
    for i in range(1,21):
        # print(i)
        cur.execute("insert into schedule (teamid) values(?)",(i,))

def insert_into_schedule(con, home_id, rand_num, other_team):
    cur = con.cursor()
    week_str = "week_" + str(rand_num)
    print(week_str)
    print(other_team)
    command_line = f'update schedule set {week_str} = ? where teamid = ?'
    cur.execute(command_line,(other_team, home_id))



