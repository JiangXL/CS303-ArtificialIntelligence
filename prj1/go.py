import numpy as np
import random
import time

""" AI solution for Gomoku
Description : AI chess
Input : chessboard layout
Outputh :
Version: v0.1  20181013 H.F.
ToDo:
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

    # If your are the first, this function will be used.
    def first_chess(self):
        assert self.color == COLOR_BLACK
        self.candidate_list.clear()
        #==================================================================
        #Here you can put your first piece
        #for example, you can put your piece on sun（天元）
        self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
        self.chessboard[self.candidate_list[-1][0], self.candidate_list[-1][0]] = self.color
        print(self.color)
        # take care whether first step is on sun

    # The input is current chessboard.
    def go(self, chessboard):
        #self.candidate_list.clear()
        #===============Action handle==========================================
        idx = np.where(chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        new_pos = idx[len(idx)//2]# choose middle value
        self.candidate_list.append((new_pos[0],new_pos[1]))
        print("Color: %d"%(self.color))
        # Only action when empty pos i chessboard more than 1
        if(len(idx)>1):
            #new_pos = idx[0];
            new_pos = self.descision(chessboard, idx)
        else:
            new_pos = idx[0] # choose the only one position
            print("No enough empty position")
        #===============Error handle===========================================
        # Make sure that the position in chess board is empty
        if not chessboard[new_pos[0],new_pos[1]]==0:
            new_pos = idx[len(idx)//2]         # replace with an empty position
            print("wrong")
        # Update decision into candidate_list
        print("Final position (%d, %d) "%(new_pos[0],new_pos[1]))
        print(chessboard)
        print()
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
                temp = self.pattern_evl(chessboard, point)
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

    def pattern_evl(self, chessboard, candidate_point):
        x = candidate_point[1]
        y = candidate_point[0]
        chessboard[y, x] =self.color
        #print("Checking point(%d, %d)"%(x,y))
        eval_value = 0

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
        # To do: reduce search region
        return eval_value

    # simple search to get hightest score point
    def simplesearch(self, chessboard, chess_color, idx):
        added_chessboard = chessboard.copy()
        max_score_point = idx[0]
        max_score = -1 # initial max_score
        for empty_point in idx:
            print("Searching points")
            # we need to update chessboard
            # chessboard[empty_point] = chess_color
            temp = self.evaluateState(chessboard, chess_color)
            if temp > max_score:
                max_score = temp
                max_score_point = empty_point
            chessboard[empty_point]
        return max_score_point

    # extra chess style from chess on one line
    def evaluateLine(self, chess_line, chess_color):
        print("evaluate line vuale")
        linevalue = 0  # return value
        continue_point = 0 # 连子数
        block_point = 0 # 封闭
        for i in range(0, chessboard):
            if chess_line[i] == chess_color: # 找到己方棋子
                # 还原计算
                continue_point = 1
                block_point = 0
                # check left side if exit opponent's chess
                if chess_line[i-1] == -chess_color : block_point+=1
                # check link chess
                for j in range(i+1, self.chessboard_size+1):
                    if chess_line[j] == chess_color:
                        continue_point+=1
                        i+=1
                if chess_line[i+1] == -chess_color: block_point+=1 # 边界也算冲
                linevalue+= self.mapValue(continue_point, block_point)
        return linevalue

    # maping score from chess style
    def mapValue(continue_point, block_point):
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
            if continue_point == 1 : return score_map('LIVEONE')
            elif continue_point == 2: return score_map('LIVETWO')
            elif continue_point == 3: return score_map('LIVETHREE')
            elif continue_point == 4: return score_map('LIVEFOUR')
            else: return score_map('LINEFIVE')
        elif block_point == 1:
            print("眠")
            if continue_point == 1 : return score_map('BLOCKED_ONE')
            elif continue_point == 2: return score_map('BLOCKED_TWO')
            elif continue_point == 3: return score_map('BLOCKED_THREE')
            elif continue_point == 4: return score_map('BLOCK_FOUR')
            else: return score_map('LINEFIVE')
        else: # both two side are opponent's chess
            print("死")
            if continue_point>= 5: return score_map('LINEFIVE')
            else: return score_map('DEADZERO')
    # calculate the total score of AI or user
    def evaluateState(self, chessboard, chess_color):
        print("Evaluate ")
        value = 0
        line = np.zeros([6, self.chessboard_size+1])
        # For the convience to check edge
        line[:, 0] = -chess_color
        line[:,-1]= -chess_color
        for i in range(0,self.chessboard_size):
            lineP = 0
            line[0,1:-2] = chessboard[i,:] # --
            line[1,1:-2] = chessboard[:,i] # |
            #line[2, ]
            region = 6
            if i==0 : region = 4
            for line_no in range(0, region):
                value += self.evaluateLine(line[line_no], chess_color)
        return value
