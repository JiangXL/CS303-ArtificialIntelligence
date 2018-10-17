import numpy as np
import random
import time

""" AI solution for Gomoku
Description : AI chess
Input : chessboard layout
Outputh : next chess localtion
Version: v0.3  20181016 H.F. Alphabeta Searching
ToDo: Use minmax
"""

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)
#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use,
        self.time_out = time_out
        # System will get the end of your candidate_list as your decision
        self.candidate_list = []
        # flag of each layout, mean remining steps
        self.live4_flag = 0 # live4 flag
        self.biflush4_flag = 0 #Double flush four
        self.max_credit = 1023
        self.defence5line_credit = 1000
        self.live4_credit = 900
        self.defence4live_credit = 850
        self.double3_credit = 800
        self.defence3double_credit = 750
        self.debug = 0
        self.chessboard = np.zeros((chessboard_size,chessboard_size), dtype=np.int)

    # If your are the first, this function will be used.
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        if self.debug : print(self.chessboard)
        #==================================================================
        #Here you can put your first piece
        #for example, you can put your piece on sun（天元）
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color
        if self.debug : print(self.color)
        if self.debug : print(self.chessboard)
        # take care whether first step is on sun

    # The input is current chessboard.
    def go(self, chessboard):
        self.candidate_list.clear()
        #===============Action handle==========================================
        idx = np.where(chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        new_pos = idx[len(idx)//2]# choose middle value
        self.candidate_list.append((new_pos[0],new_pos[1]))
        if self.debug : print("Color: %d"%(self.color))
        # Only action when empty pos i chessboard more than 1
        if(len(idx)>1):
            #new_pos = idx[0];
            new_pos = self.descision(chessboard, idx)
            #new_pos = self.simpleSearch(chessboard, self.color, idx)
            #print(new_pos)
        else:
            new_pos = idx[0] # choose the only one position
            if self.debug : print("No enough empty position")
        #===============Error handle===========================================
        # Make sure that the position in chess board is empty
        if not chessboard[new_pos[0],new_pos[1]]==0:
            new_pos = idx[len(idx)//2]         # replace with an empty position
            if self.debug : print("wrong")
        # Update decision into candidate_list
        if self.debug : print("Final position (%d, %d) "%(new_pos[0],new_pos[1]))
        if self.debug : print(chessboard)
        if self.debug : print()
        self.candidate_list[-1]=((new_pos[0],new_pos[1]))

    # Find out next position
    def descision(self, chessboard, idx):
        print("Descising...")
        #search_box=
        # Deal some layout needn't search
        if self.live4_flag>0 :
            #choose_pos=live4solver(chessboard)
            print("live4")
        elif self.biflush4_flag > 0:
            print("Double flush four")
            #choose_pos=self.biflush4solver(chessboard)
        else:
            print("Searching...")
            # find highest score point
            max_candidate = -1              # trick value to avoid initial case
            for point in idx:
                #temp = self.pattern_evl(chessboard, point)
                temp = self.alphaBeta(chessboard, 2, - 999999999, +999999999, self.color)
                if temp == self.max_credit:                    # largest credit
                    choose_pos= point
                    #print("Found largest credit %d %d"%(choose_pos[0],choose_pos[1]))
                    break
                elif temp > max_candidate:
                    max_candidate = temp
                    choose_pos= point
                    #print("Find larger credit %d %d"%(choose_pos[0],choose_pos[1]))
        #choose_pos=(2,2)
        return choose_pos

    def nextMove(self, source_chessboard):
        no_empty = 0
        empty_point = np.where(source_chessboard == 0)
        empty_point = list(zip(empty_point[0], empty_point[1]))
        if len(empty_point) == 1: no_empty = 1
        next_pos = empty_point[len(empty_point)//2]# choose middle value
        # sort the point return max point position

        '''
        line5 = self.line5detect(chessboard, x, y)
        if line5 :
            eval_value = line5
        else:
            live4 = self.live4detect(chessboard, x, y)
            if live4:
                eval_value = live4
            else:
                double3 = self.double3detect(chessboard, x, y)
                if double3:
                    eval_value = double3
        '''
        # To do: reduce search region
        return no_empty, next_pos

    def movesLeft(self, source_chessboard):
        empty_point = np.where(source_chessboard == 0)
        empty_point = list(zip(empty_point[0], empty_point[1]))
        return len(empty_point)

    def alphaBeta(self, source_chessboard, depth, alpha, beta, chess_color):
        is_full_pos, next_pos = self.nextMove(source_chessboard)
        print("search pint %d %d"%(next_pos[0], next_pos[1]))
        if depth == 0 or is_full_pos: # or no empty position
            print("Test label")
            return self.evaluateState(source_chessboard, chess_color)-self.evaluateState(source_chessboard, chess_color)
        else:
            #updated_chessboard = source_chessboard.copy()
            while self.movesLeft(source_chessboard):
                #updated_chessboard[next_pos[0],next_pos[1]] = chess_color
                source_chessboard[next_pos[0],next_pos[1]] = chess_color
                weight = - self.alphaBeta(source_chessboard, depth -1, -beta, -alpha, chess_color)
                #UnmakeMove()?
                #del updated_chessboard
                source_chessboard[next_pos[0],next_pos[1]] = 0
                if weight >= beta :
                    return beta
                if weight > alpha :
                   alpha = weight
            return alpha

    # simple search to get hightest score point
    def simpleSearch(self, current_chessboard, chess_color, idx):
        added_chessboard = current_chessboard.copy() # H.F.: It may increase cost
        max_score_point = idx[0]
        max_score = -10000000 # initial max_score
        for empty_point in idx:
            # we need to update chessboard
            added_chessboard[empty_point[0],empty_point[1]] = chess_color
            #print("Simple Searching points")
            temp = self.evaluateState(added_chessboard, chess_color)-self.evaluateState(added_chessboard, -chess_color)
            if temp > max_score:
                max_score = temp
                max_score_point = empty_point
                if self.debug : print("Score %d Point %s"%(temp, empty_point))
                #temp2 = self.evaluateState(added_chessboard, -chess_color)
                #print("Score -%d"%(temp2))
                #print(added_chessboard)
            #print(max)
            added_chessboard[empty_point[0],empty_point[1]] = 0
        return max_score_point

    # calculate the total score of AI or user
    def evaluateState(self, chessboard, chess_color):
        #print("Evaluate current chessboard state")
        value = 0
        line = np.zeros([6, self.chessboard_size+2])
        # For the convience to check edge
        line[:, 0] = -chess_color
        line[:,-1]= -chess_color
        #print(line[:,-1])
        #print(line)
        for i in range(0, self.chessboard_size):
            # scan in four directions
            lineP = 0
            line[0, 1:-1] = chessboard[i,:] # --
            line[1,1:-1] = chessboard[:,i] # |
            for j in range(0, self.chessboard_size):
                # HF: need to deal with condition: chess nubmer less than size
                if i+j<self.chessboard_size: # \
                    line[2, j+1] = chessboard[i+j, j] # \ (down region)
                    line[4, j+1] = chessboard[j, i+j] # \ (up region)
                    line[5, j+1] = chessboard[self.chessboard_size-j-1, i+j]
                else:
                    line[2, j+1] = -chess_color
                    line[4, j+1] = -chess_color
                    line[5, j+1] = -chess_color
                if i-j>-1: # /
                    line[3, j+1] = chessboard[i-j, j] # / (up region)
                else:
                    line[3, j+1] = -chess_color
            # evaluate the value
            region = 6 # avoid add the diagose line twice
            if i==0 : region = 4
            for line_no in range(0, region):
                #print("Value: %d"%value)
                value += self.evaluateLine(line[line_no], chess_color)
            #print("State Value: %d"%(value))
            #print(line)
        #print(value)
        return value

    # extra chess style from chess on one line
    def evaluateLine(self, chess_line, chess_color):
        #print("Evaluate line vuale")
        linevalue = 0  # return value
        continue_point = 0 # 连子数
        block_point = 0 # 封闭
        # scan chess line to find style
        i = 0
        while(i<self.chessboard_size):
        #for i in range(0, self.chessboard_size):
            #print(i)
            if chess_line[i] == chess_color: # 找到己方棋子
                # 还原计算
                continue_point = 1
                block_point = 0
                # check left side if exit opponent's chess
                if chess_line[i-1] == -chess_color : block_point+=1
                # check linked chess
                i+=1
                while (i<self.chessboard_size and chess_line[i] == chess_color):
                    i+=1
                    continue_point+=1
                if chess_line[i] == -chess_color: block_point+=1 # 边界也算冲
                #print("Label%d %d"%(continue_point, block_point))
                linevalue += self.mapValue(continue_point, block_point)
            i+=1
        return linevalue

    # maping score from chess style
    def mapValue(self, continue_point, block_point):
        #print("Map chess style to value")
        score_map={'DEADZERO': 0,
                   'LIVEONE': 10,
                   'LIVETWO': 100,
                   'LIVETHREE': 1000,
                   'LIVEFOUR': 100000,
                   'LINEFIVE': 10000000,
                   'BLOCKED_ONE': 1,
                   'BLOCKED_TWO': 10,
                   'BLOCKED_THREE': 100,
                   'BLOCK_FOUR': 10000}
        if block_point == 0:
            #print("活")
            if continue_point == 1 : return score_map['LIVEONE']
            elif continue_point == 2: return score_map['LIVETWO']
            elif continue_point == 3: return score_map['LIVETHREE']
            elif continue_point == 4: return score_map['LIVEFOUR']
            else: return score_map['LINEFIVE']
        elif block_point == 1:
            #print("眠")
            if continue_point == 1 : return score_map['BLOCKED_ONE']
            elif continue_point == 2: return score_map['BLOCKED_TWO']
            elif continue_point == 3: return score_map['BLOCKED_THREE']
            elif continue_point == 4: return score_map['BLOCK_FOUR']
            else: return score_map['LINEFIVE']
            #print("Test label")
        else: # both two side are opponent's chess
            #print("死")
            if continue_point>= 5: return score_map['LINEFIVE']
            else: return score_map['DEADZERO']
