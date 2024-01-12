import itertools
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
def get_team_info_from_id(con, id):
    cur = con.cursor()
    team_info = cur.execute("select * from teams where teams.teamid = ?",(id,))
    return team_info

def generate_schedule(con):

    cur_read = con.cursor()
    cur_write = con.cursor()
    teams = cur_read.execute("select teams.name from teams")
    # schedule = cur_read.execute("select * from schedule")
    number = 1
    teams_j = open("teams.json")
    teams_j = json.load(teams_j)


    print(teams_j)
    lst_teams = []
    for i in teams_j['teams']:
        lst_teams.append(i)
    # print(lst_teams)


    #Creating the dict for total schedule
    total_schedule = {}
    for i in lst_teams:
        total_schedule[i] = []
        for j in range(38):
            total_schedule[i].append(None)
        # print(total_schedule)



    for i in range(len(lst_teams)):

        """Create a list without the team we are picking for
        For example, Arsenal wouldn't play Arsenal etc..."""
        pick_teams = lst_teams[:i] + lst_teams[i + 1:]

        """Double the list"""
        pick_teams *=2

        # print(pick_teams)
        home_team = lst_teams[i]
        # print(f'Home Team: {home_team}')
        team_query = get_team_info(con, home_team)
        # print(team_query.fetchall())
        # team_query = (team_id, team_name, other_info...)
        # Example: (14, Manchester United, 5, 14, 19, 95)
        team_id = team_query.fetchone()[0]
        team_query = get_team_info(con,home_team)
        team_name = team_query.fetchone()[1]
        # print(f'Team ID: {team_id}')
        # print(f'Team Name: {team_name}')
        # team_query = get_team_info(con, home_team) # This will be for the away team potentially



        """Swapping the teams in the pick list"""
        for j in range(len(pick_teams)):
            rnd = random.randint(0, len(pick_teams)-1)
            # print(f'Rand: {rnd}')
            temp = pick_teams[rnd]

            # Swap teams with random index
            pick_teams[rnd] = pick_teams[j]
            pick_teams[j] = temp


        """This is where I'm going to edit the dictionary to act like the sql stuff"""
        iterations = 0
        for k in range(len(pick_teams)):
            # print(f'What is this {home_team}? {total_schedule[home_team][k]}')
            iterations+=1
            # print(f'Iteration: {iterations}')

            """If both teams have an empty slot"""
            if total_schedule[home_team][k] == None and total_schedule[pick_teams[k]][k] == None:
                # print("Is this being executed?")
                # print(total_schedule)
                # total_schedule[home_team].append(pick_teams[k])
                # total_schedule[pick_teams[k]].append(home_team)
                total_schedule[home_team][k] = pick_teams[k]
                total_schedule[pick_teams[k]][k] = home_team
            # else:
            #     while total_schedule[home_team][k] is None and total_schedule[pick_teams[k]][k] is None:


        # print(total_schedule)
        for team in total_schedule:
            # print(f'{team} : {total_schedule[team]}')
            team_query = get_team_info(con, team)
            team_id = team_query.fetchone()[0]
            team_query = get_team_info(con, team)
            team_name = team_query.fetchone()[1]
            week = 1
            for opponent in total_schedule[team]:
                insert_into_schedule(con,team_id,week,opponent,cur_write)
                week+=1
    week = 1
    for i in range(1,39):
        print(f'WEEK {week} NOOPS---------')
        week_str = "week_" + str(week)
        command_line = f'select teamid, {week_str} from schedule where {week_str} is Null'
        schedule_query = cur_read.execute(command_line)
        noop_list = schedule_query.fetchall()
        print(noop_list)
        # print(len(noop_list))
        # print(noop_list[0][0])
        for j in range(0,len(noop_list),2):
            #Go through teamid order, and team below teamid plays above, final teamid in list plays above

            team_query = get_team_info_from_id(con,noop_list[j][0])
            team_info = team_query.fetchone()
            team_name = team_info[1]
            team_id = team_info[0]
            # print(f'Home: {team_name} ID: {team_id}')
            """Executing a sql query and storing it in away_team_query"""
            away_team_query = get_team_info_from_id(con,noop_list[j+1][0])

            """Store the tuple inside away_team_info(by only fetching one)"""
            away_team_info = away_team_query.fetchone()

            """Take tuple and disperse the data appropriately"""
            away_team_name = away_team_info[1]
            away_team_id = away_team_info[0]


            # print(f'Away: {away_team_name} ID: {away_team_id}')
            """Update the spot for home team"""
            insert_into_schedule(con,team_id,week,away_team_name,cur_write)
            """Update the spot for away team"""
            insert_into_schedule(con, away_team_id,week,team_name,cur_write)
            # print(team_name)
        week+=1




"""Inserts teamid values into schedule datatable"""
def generate_initial_schedule_value(cursor):
    cur = cursor
    #Generate all of the team_ids
    for i in range(1,21):
        # print(i)
        cur.execute("insert into schedule (teamid) values(?)",(i,))

def insert_into_schedule(con, home_id, week_num, other_team,cursor_write):
    cur = con.cursor()
    week_str = "week_" + str(week_num)
    # print(week_str)
    # print(other_team)
    command_line = f'update schedule set {week_str} = ? where teamid = ?'
    cursor_write.execute(command_line,(other_team, home_id))
    # con.commit()




