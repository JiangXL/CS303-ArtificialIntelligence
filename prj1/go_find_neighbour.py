import numpy as np
import random
import time
import pdb
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
        self.debug = 1
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
        print("run go")
        self.candidate_list.clear()
        #===============Action handle==========================================
        idx = np.where(chessboard == 0)
        idx = list(zip(idx[0], idx[1]))
        new_pos = idx[len(idx)//2]# choose middle value
        self.candidate_list.append((new_pos[0],new_pos[1]))
        if self.debug : print("Color: %d"%(self.color))
        # Only action when empty pos i chessboard more than 1
        if(len(idx) == self.chessboard_size*self.chessboard_size):
            self.first_chess
        elif(len(idx)>1):
            #new_pos = idx[0];
            #new_pos = self.descision(chessboard, idx)
            new_pos = self.finalSearch(chessboard, self.color, idx)
            print(new_pos)
        else:
            new_pos = idx[0] # choose the only one position
            if self.debug : print("No enough empty position")
        #===============Error handle===========================================
        # Make sure that the position in chess board is empty
        if not chessboard[new_pos[0],new_pos[1]]==0:
            new_pos = idx[len(idx)//2]         # replace with an empty position
            if self.debug : print("wrong")
        # Update decision into candidate_list
        if self.debug : print("Final position (%d, %d)"%(new_pos[0],new_pos[1]))
        if self.debug : print(chessboard)
        if self.debug : print()
        #self.candidate_list[-1]=((new_pos[0],new_pos[1]))
        self.candidate_list.append((new_pos[0],new_pos[1]))

    # Final search to get hightest score point
    def finalSearch(self, current_chessboard, chess_color, idx):
        added_chessboard = current_chessboard.copy() # H.F.: It may increase cost
        max_score_point = idx[0]
        max_score = -1000000000 # initial max_score
        empty_points = np.where(added_chessboard == 0)
        empty_points = self.genNext(added_chessboard)
        print(len(idx))
        if len(idx) > self.chessboard_size*self.chessboard_size-5:
            print("Simple")
            for empty_point in idx:
                added_chessboard[empty_point[0], empty_point[1]] = chess_color
                #print("Simple Searching points")
                score = (self.evaluateState(added_chessboard, chess_color)
                    -self.evaluateState(added_chessboard, -chess_color))
                if score > max_score:
                    max_score = score
                    max_score_point = empty_point
                    if self.debug : print("Score %d Point %s"%(score, empty_point))
                added_chessboard[empty_point[0], empty_point[1]] = 0
        else :
            if self.debug: print("minMax")
            start = time.time()
            for empty_point in empty_points:
                added_chessboard[empty_point[0], empty_point[1]] = chess_color
                score = self.alphaBeta(added_chessboard, 1, -99999999, 99999999, chess_color)
                #score = self.alphaBeta(added_chessboard, 1, max_score, 99999999, chess_color)
                #if self.debug: print("Final Score %d"%(score))
                #input("continue?")
                # from next
                if score > max_score:
                    max_score = score
                    max_score_point = empty_point
                    if self.debug : print("Score %d Point %s"%(score, empty_point))
                added_chessboard[empty_point[0], empty_point[1]] = 0
            print("alphaBeta time cost: %d"%(time.time()-start))
        return max_score_point

    # Find out next position set
    def genNext(self, source_chessboard):
        #input("genNext?")
        #print(source_chessboard)
        pos = np.where(source_chessboard != 0)
        pos_package = list(zip(pos[0], pos[1]))
        '''
        edge_cl = min(pos[1])
        if edge_cl-2 < 0 :
            edge_cl =0
        else:
            edge_cl = edge_cl - 2
        edge_cr = max(pos[1])
        if edge_cr + 2 > self.chessboard_size-1:
            edge_cr = self.chessboard_size-1
        else:
            edge_cr = edge_cr + 2
        edge_ru = min(pos[0])
        if edge_ru-2 < 0 :
            edge_ru =0
        else:
            edge_ru = edge_ru - 2
        edge_rd = max(pos[0])
        if edge_rd + 2 > self.chessboard_size-1:
            edge_rd = self.chessboard_size-1
        else:
            edge_rd = edge_rd + 2
        #print("row: %d-%d col: %d-%d"%(edge_ru, edge_rd, edge_cl, edge_cr))
        empty_points = np.where(source_chessboard[edge_ru:edge_rd+1, edge_cl:edge_cr+1] == 0)
        empty_points = list(zip(empty_points[0]+edge_ru, empty_points[1]+edge_cl))
        '''

        # find positon with chess
        neighbor_points = []
        for chess in pos_package:
            for i in [-2,-1,1,2]:
                for j in [-2,-1,1,2]:
                    new_pos0 = chess[0]+i
                    new_pos1 = chess[1]+j
                    if new_pos0 > self.chessboard_size-1:
                        new_pos0 = self.chessboard_size-1
                        #print("new_pos0>14: %d"%(new_pos0))
                    elif new_pos0 < 0 :
                        new_pos0 = 0
                    if new_pos1 > self.chessboard_size-1:
                        new_pos1 = self.chessboard_size-1
                    elif new_pos1 < 0:
                        new_pos1 = 0
                    new_pos = (new_pos0, new_pos1)
                    #print("%d %d"%(new_pos0, new_pos1))
                    if (new_pos not in neighbor_points
                            and new_pos not in pos_package ):
                        neighbor_points.append( new_pos)
                        #print("neighbor_point: (%d, %d)"%(neighbor_points[-1][0], neighbor_points[-1][1]))
        #print("new_pos: %d"%(len(neighbor_points)))
        # sort the point return max point positio
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
        #return empty_points
        return neighbor_points

    # alphabeta pruching
    def alphaBeta(self, source_chessboard, depth, alpha, beta, chess_color):
        #input("continue?")
        if depth == 0 : # or no empty position
            #print("final")
            #if self.debug: print(source_chessboard)
            #if self.debug: print(chess_color)
            #temp = self.evaluateState(source_chessboard, chess_color)
            temp= (self.evaluateState(source_chessboard, chess_color)
                -self.evaluateState(source_chessboard, -chess_color))
            #temp=temp*chess_color
            #if self.debug: print("Now node score: %d"%(temp))
            return temp
        else:
            updated_chessboard = source_chessboard.copy()
            candidate_points = self.genNext(updated_chessboard)
            #print("Len: %d depth: %d"%(len(candidate_points), depth))
            weight = -9999999999  # smallest number
            for point in candidate_points :
                #print("search print %d %d"%(point[0], point[1]))
                updated_chessboard[point[0], point[1]] = -chess_color
                #weight = max(weight, -self.alphaBeta(updated_chessboard, depth-1, -beta,-alpha, -chess_color))
                weight = max(weight, self.alphaBeta(updated_chessboard, depth-1, -beta,-alpha, -chess_color))
                #print("Weight: %d"%(weight))
                updated_chessboard[point[0], point[1]] = 0
                alpha = max(alpha, weight)
                if alpha >= beta:
                    break
            del updated_chessboard
        #return beta # 对方最小得分
        return chess_color*weight # 对方最小得分
        #return weight

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
