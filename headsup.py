from cards import *
from hand_evaluator import *
import time
import copy
import urllib2
import random



class HeadsUp:
    players = 2
    deck = []
    ante = 1
    blinds = [1,2] ## small blind and big blind is 1 and 2
    total_bank_roll = [200, 200] ## this is what the players have at the very beginning
    # first belongs to cepheus and the second one belongs to player
    rounds = 4 # preflop, blabla, I am not gonna use what is inside the pycfr package cause it is too complicated
    maxbets = 4 # you don't have to initialize all these maxbets
    bet_his = []
    # you know how to use bet history

    def __init__(self):
        players = 2
        deck = []
        ante = 1
        blinds = [1,2] ## small blind and big blind is 1 and 2
        total_bank_roll = [200, 200] ## this is what the players have at the very beginning
        rounds = 4 # preflop, blabla, I am not gonna use what is inside the pycfr package cause it is too complicated
        bet_his = []

    # as this is about AI we only consider the position of cepheus now.
    # which means that all the position 
        
    def checkStatus(self):
        for i in total_bank_roll:
            if i <= 0:
                return "Terminated"
        else return "OnGoing"
