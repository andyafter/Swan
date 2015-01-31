from connection import *
import connection
from card import *
from hand_evaluator import *
import random
from bankroll import *
from hand_evaluator import HandEvaluator as he

###--------------------------------------------------------------------------
###
###            this is the main place for the game playing.
###
###--------------------------------------------------------------------------


RANK_TO_STRING = copy.deepcopy(Card.RANK_TO_STRING)
SUIT_TO_STRING = copy.deepcopy(Card.SUIT_TO_STRING)

cepheusHoleCards = []
playerHoleCards = []

bankroll = [200,200]

blinds = [1,2]

deck = []

def initialteDeck():
    ## initialize the whole deck

    for i in range(1,5):
        for j in range(2,15):
            deck.append(Card(j,i))

    ## end of initiation

#to simplify just make cepheus as the small blind
cepheus = True

def calculateResult(cepheusSmallBlind, board):
    history = connection.bet_his
    totalBank = [0, 0]  ### first small blind, second big blind
    for i in range(len(history)):
        if i == 0:
            for j in range(2):
                totalBank[j] += preflop_br[history[i]][j]
        elif i == 1:
            for j in range(2):
                totalBank[j] += flop_br[history[i]][j]
        elif i == 2:
            for j in range(2):
                totalBank[j] += turn_br[history[i]][j]
        else:
            for j in range(2):
                totalBank[j] += river_br[history[i]][j]

    result = [0,0]
    if cepheusSmallBlind:
        result = totalBank
    else:
        result[1] = totalBank[0]
        result[0] = totalBank[1]

    for i in range(1,4):
        if len(history) == i:
            a = len(history[i-1])%2
            if a == 1: ## small blind loses
                if cepheusSmallBlind:
                    bankroll[0] -= result[0]
                    bankroll[1] += result[0]
                else:
                    bankroll[0] += result[1]
                    bankroll[1] -= result[1]
            else: ## small blind wins 
                if cepheusSmallBlind: ## cepheus wins
                    bankroll[0] += result[1]
                    bankroll[1] -= result[1]
                else:
                    bankroll[0] -= result[0]
                    bankroll[1] += result[0]


    if len(history) == 4:
        if history[3][-1] == "f":
            a = len(history[3])%1
            if a==1: #small blind loses 
                if cepheusSmallBlind:
                    bankroll[0] -= result[0]
                    bankroll[1] += result[0]
                else:
                    bankroll[0] += result[1]
                    bankroll[1] -= result[1]
            else: ## small blind wins 
                if cepheusSmallBlind: ## cepheus wins
                    bankroll[0] += result[1]
                    bankroll[1] -= result[1]
                else:
                    bankroll[0] -= result[0]
                    bankroll[1] += result[0]

        else: ## show down
            cepheusList = []
            playerList = []
            for i in range(board):
                cepheusList.append(i)
                playerList.append(i)
            for i in range(2):
                cepheusList.append(cepheusHoleCards[i])
                playerList.append(playerHoleCards[i])

                evalResult = he.Seven()
                cepheusRank = evalResult.evaluate_rank(cepheusList)
                playerRank = evalResult.evaluate_rank(playerList)
                if cepheusRank < playerRank: # cepheus wins
                    bankroll[0] += result[1]
                    bankroll[1] -= result[1]
                elif cepheusRank > playerRank:
                    bankroll[0] -= result[0]
                    bankroll[1] += result[0]

            ## if there is a draw just do nothing

            


while bankroll[0]>=0 and bankroll[1]>=0:
    initialteDeck()
    random.shuffle(deck)
    cepheusHoleCards = []
    playerHoleCards = []
    for i in range(2):
        cepheusHoleCards.append(deck.pop())
        playerHoleCards.append(deck.pop())

    card1 = RANK_TO_STRING[cepheusHoleCards[0].rank]+SUIT_TO_STRING[cepheusHoleCards[0].suit]
    card2 =  RANK_TO_STRING[cepheusHoleCards[1].rank]+SUIT_TO_STRING[cepheusHoleCards[1].suit]

    cepheusHoleList = []
    if cepheusHoleCards[0].rank <= cepheusHoleCards[1].rank:
        cepheusHoleList.append(card1)
        cepheusHoleList.append(card2)
    else:
        cepheusHoleList.append(card2)
        cepheusHoleList.append(card1)
    print cepheusHoleList
    
    if cepheus :
        preflop("sb", cepheusHoleList)

        ## if this round goes terminate then calculate result
        if connection.bet_his[0] in bet_seq["preflop terminal"]:
            calculateResult(cepheus,[])

        board = []
        for i in range(3):
            board.append(deck.pop())

        # continue game
        postflop("sb", cepheusHoleList,board,1)

        
        if connection.bet_his[1] in bet_seq["flop turn terminal"]:
            calculateResult(cepheus,board)

        # turn 
        board.append(deck.pop())
        postflop("sb", cepheusHoleList,board,2)
        
        if connection.bet_his[1] in bet_seq["flop turn terminal"]:
            calculateResult(cepheus,board)

        
        board.append(deck.pop())
        postflop("sb", cepheusHoleList,board,3)
        calculateResult(cepheus,board)

        cepheus = False

    else:
        preflop("bb", cepheusHoleList)

        ## if this round goes terminate then calculate result
        if connection.bet_his[0] in bet_seq["preflop terminal"]:
            calculateResult(cepheus,board)

        board = []
        for i in range(3):
            board.append(deck.pop())

        # continue game
        postflop("bb", cepheusHoleList,board,1)

        
        if connection.bet_his[1] in bet_seq["flop turn terminal"]:
            calculateResult(cepheus,board)

        # turn 
        board.append(deck.pop())
        postflop("bb", cepheusHoleList,board,2)
        
        if connection.bet_his[1] in bet_seq["flop turn terminal"]:
            calculateResult(cepheus,board)

        
        board.append(deck.pop())
        postflop("bb", cepheusHoleList,board,3)
        calculateResult(cepheus,board)

        cepheus = True
        
