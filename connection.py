import random
import urllib2
import httplib
from card import *
from hand_evaluator import *
import time
import copy
#from headsup import *


# in the poker cards, 1 is s, 2: h, 3: d, 4: c
# in the above simply use the SUIT_TO_STRING

SUIT_TO_STRING = Card.SUIT_TO_STRING
RANK_TO_STRING = Card.RANK_TO_STRING


## this here defines all the information that is needed for the poker rule
players = 2
deck = []
ante = 1
bet_his = []
blinds = [1,2] ## small blind and big blind is 1 and 2
total_bank_roll = [200, 200] ## this is what the players have at the very beginning
rounds = 4 # preflop, blabla, I am not gonna use what is inside the pycfr package cause it is too complicated
##

bet_seq = {}
bet_seq["preflop continuing"] = ["cc", "crc", "crrc", "crrrc", "rc", "rrc", "rrrc"]
bet_seq["preflop terminal"] = ["f", "rf", "rrf", "rrrf", "crf", "crrf", "crrrf"]
bet_seq["flop turn continuing"] = ["cc", "crc", "crrc", "crrrc", "crrrrc", "rc", "rrc", "rrrc", "rrrrc"]
bet_seq["flop turn terminal"] = ["rf", "rrf", "rrrf", "rrrrf", "crf", "crrf", "crrrf", "crrrrf"]
bet_seq["river continuing"] = ["cc", "crc", "crrc", "crrrc", "crrrrc", "rc", "rrc", "rrrc", "rrrrc"]
bet_seq["river terminal"] = ["cc", "rc", "rf", "rrc", "rrf", "rrrc", "rrrf", "rrrrc", "rrrrf", "crc", "crf", "crrc", "crrf", "crrrc", "crrrf", "crrrrc", "crrrrf"]
 
action = ['f', 'c', 'r']



# write a function to generate url string according to the game status


def genURL(r, boardString): ## r is the round number starts with 0, where 0 means preflop
    # here the bet history is a list of length r+1
    # here board is a string and you know what to do
    ori = "http://poker.srv.ualberta.ca/query?queryString="
    temp = ""

    for i in range(r+1):
        temp = temp + bet_his[i]

        ####  change here 
        if i == r:
            temp = temp + "%3A"
        else:
            if bet_his[i+1]!= "":
                temp = temp + "%2F"
    temp = temp+boardString
            
    print temp
    print ori+temp
    return ori + temp

def genStrategy(URL, cepheusHoleCards):
    #cepheusHoleCards is a string like what is inside the content
    # assume that cepheus
    
    content = urllib2.urlopen(URL).read()
    a = content.split()
    b = copy.deepcopy(a[3:])

    hole = cepheusHoleCards[0] + cepheusHoleCards[1]
    ind = b.index(hole)
    Fold =  float(b[ind + 1])
    Call =  float(b[ind + 2])
    Raise =  float(b[ind + 3])
    rand = random.random()
    if rand <= Fold:
        return "f"
    elif rand> Fold and rand <=(Fold + Call):
        return "c"
    else:
        return "r"


def preflop(blindStatus, cepheusHoleCards):
    while len(bet_his)>0:
        bet_his.pop()
    # initialte inside 
    bet_his.append("")
    #blindStatus is a string indicates what blind position is cepheus
    bets = 0

    
    ## if cepheus equals True then it's cepheus's turn to act
    cepheus = False
    # betTotal = blinds[1] ## this is the largest bet size on board

    ## here the if sentense is only here to help choose the small blind people
    if blindStatus == "sb":
        cepheus = True
    

    ################
    #############
    #### check if this logic is right
        
    while True:
        print bet_his
        if cepheus:
            URL = genURL(0,"")
            strategy = genStrategy(URL, cepheusHoleCards)
            bet_his[0] += strategy
            cepheus = not cepheus

            if strategy == 'f':
                break
            elif strategy == 'c':
                if len(bet_his[0]) == 0:
                    continue
                break
            else:
                bets += 1
                continue
            
        else:
            playerStrategy = raw_input('Act:')
            # to prevent you from been confused I set the strategy name as a different one.

            
            if playerStrategy not in action:
                continue

            bet_his[0] += playerStrategy
            cepheus = not cepheus # this is important
            if playerStrategy == 'f':
                break
            elif playerStrategy == 'c':
                # if there is no history then big blind has a chance to act
                if len(bet_his[0]) == 0:
                    continue

                
                break
            else:
                bets += 1
                continue
    # the return value is the last action here

        print "current status"
        print bet_his
    return bet_his[0][-1]


def board2String(board):
    temp = ""
    for i in board:
        temp+= RANK_TO_STRING[i.rank]
        temp+= SUIT_TO_STRING[i.suit]

    return temp


def postflop(blindStatus, cepheusHoleCards, board, r):
    # r is the number round starts from 0
    if r == 1:
        print "flop"
    elif r == 2:
        print "turn"
    elif r == 3:
        print "river"
    
    bet_his.append("")
    print bet_his
    bets = 0
    cepheus = False

    if blindStatus == "sb":
        cepheus = True

    while True:
        if cepheus:
            URL = genURL(r,board2String(board))
            strategy = genStrategy(URL,cepheusHoleCards)
            bet_his[r] += strategy
            cepheus = not cepheus

            if strategy == 'f':
                break
            elif strategy == 'c':
                if len(bet_his[r]) == 0:
                    continue
                break
            else:
                bets += 1
                continue
            
        else:
            playerStrategy = raw_input('Act:')
            # to prevent you from been confused I set the strategy name as a different one.

            
            if playerStrategy not in action:
                continue

            bet_his[r] += playerStrategy
            cepheus = not cepheus
            if playerStrategy == 'f':
                break
            elif playerStrategy == 'c':
                # if there is no history then big blind has a chance to act
                if len(bet_his[r]) == 0:
                    continue

                
                break
            else:
                bets += 1
                continue
    # the return value is the last action here
        print "current status"
        print bet_his
    return bet_his[r][-1]
