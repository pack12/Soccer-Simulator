#How do we create a match

"""
A match can be an object potentially that is initialized with two teams
We have to assign who is the home team or who is the away team
match needs to calculate each team's final rating, the rating system will not be anything special, it will just be...
who has the higher overall rating after calculating the ratings. Kind of like War (the card game)

What is the luck modifier? Well it's something that can either help a team or really make a team struggle
We also need to make a goal engine? Where the difference of ratings, determines how many goals are scored in a game

Or we simply just have it so that one team 'Wins' over another team (but that's boring)
If we're modeling soccer, maybe the best approach is to just do a random dice throw approach?

"""
import random


class Match:
    def __init__(self,team1,team2):
        self.home = team1
        self.away = team2
        self.home_luck = 0
        self.away_luck = 0


    def decide_winner(self):
        if self.home.sum_rating + self.home.luck_rating > self.away.sum_rating + self.away.luck_rating:
            self.home.winner = True
            self.away.winner = False
        else:
            self.away.winner = True
            self.home.winner = False



