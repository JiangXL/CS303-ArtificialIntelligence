#!/usr/bin/env python3
"""
check the security and functionability of uploaded code
- forbid from importing os
- random chessboard check
- some special case check
"""
import traceback
import sys
import numpy as np
from go import AI

if __name__ == '__main__':
    #code_checker = CodeCheck("Your code address", 15
    chessboard_size = 15
    color = -1
    time_out = 5
    gomoku_ai = AI(chessboard_size, color, time_out)

    #chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)

    chessboard = np.zeros((chessboard_size, chessboard_size), dtype=np.int)
    chessboard[2, 2] = 1
    chessboard[3, 3] = 1
    chessboard[4, 4] = 1
    chessboard[5, 6] = 1
    chessboard[5, 8] = 1
    chessboard[1:3, 11] = -1
    chessboard[3, 9:11] = -1
    chessboard[6, 13] = -1
    print(chessboard)

    chessboard[3, 11] = color
    chessboard[1, 1] = -color
    score= (gomoku_ai.evaluateState(chessboard, color)
        -gomoku_ai.evaluateState(chessboard, -color))
    print(score)

    chessboard[1, 1] = color
    chessboard[5, 5] = -color
    score= (gomoku_ai.evaluateState(chessboard, color)
        -gomoku_ai.evaluateState(chessboard, -color))
    print(score)

    '''
    gomoku_ai.go(chessboard)

    result = gomoku_ai.candidate_list[-1]
    chessboard[result[0],result[1]]= color
    print(chessboard)

    for i in range(0, 10):
        user_0, user_1 = map(int, input('User: ').split())
        chessboard[user_0, user_1] = -color
        print(chessboard)

        gomoku_ai.go(chessboard)
        result = gomoku_ai.candidate_list[-1]
        chessboard[result[0],result[1]]= color
        print("AI: (%d %d)"%(result[0],result[1]))
        print(chessboard)
    '''
