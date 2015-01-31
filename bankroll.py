### this is simply to make a hash from betting sequence to bankroll chance

## every betting sequence is the key and the value is a list consists of two numbers,
## two numbers indicate the money both small blind and big blind have put into the pot

import copy


preflop_br = {
    "cc"   : [2,2],
    "crc"  : [3,3],
    "crrc" : [4,4],
    "crrrc": [ 5,5,],
    "rc"   : [3,3],
    "rrc"  : [4,4],
    "rrrc" : [5,5],
    "f"    : [1,2],
    "rf"   : [3,2],
    "rrf"  : [3,4],
    "rrrf" : [5,4],
    "crf"  : [2,3],
    "crrf" : [4,3],
    "crrrf": [4,5]

    }

flop_br = {
    "cc"    : [0,0],
    "crc"   : [1,1],
    "crrc"  : [2,2],
    "crrrc" : [3,3],
    "crrrrc": [4,4],
    "rc"    : [1,1],
    "rrc"   : [2,2],
    "rrrc"  : [3,3],
    "rrrrc" : [4,4],
    "rf"    : [1,0],
    "rrf"   : [1,2],
    "rrrf"  : [3,2],
    "rrrrf" : [3,4],
    "crf"   : [0,1],
    "crrf"  : [2,1],
    "crrrf" : [2,3],
    "crrrrf": [4,3]


    }

turn_br = copy.deepcopy(flop_br)

for i in turn_br:
    turn_br[i][0] *= 2
    turn_br[i][1] *= 2

river_br = {
    "cc"    : [0,0],
    "rc"    : [2,2],
    "rf"    : [2,0],
    "rrc"   : [4,4],
    "rrf"   : [2,4],
    "rrrc"  : [6,6],
    "rrrf"  : [6,4],
    "rrrrc" : [8,8],
    "rrrrf" : [6,8],
    "crc"   : [2,2],
    "crf"   : [0,2],
    "crrc"  : [4,4],
    "crrf"  : [4,2],
    "crrrc" : [6,6],
    "crrrf" : [4,6],
    "crrrrc": [8,8],
    "crrrrf": [8,6]

}
