import numpy as np
import random
import time
import pdb
""" AI solution for Gomoku
Description : AI chess
Input : chessboard layout
Outputh : next chess localtion
Version: v0.5  20181027 H.F. Fix the genNext miss positions issue
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
        self.debug = 0
        self.chessboard = np.zeros((chessboard_size,chessboard_size), dtype=np.int)
        self.anfangtifet = 2 # initial depth

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
        if(len(idx) == self.chessboard_size*self.chessboard_size):
            self.first_chess()
        elif(len(idx)>1):
            #new_pos = idx[0];
            #new_pos = self.descision(chessboard, idx)
            #new_pos = self.finalSearch(chessboard, self.color, idx)
            self.alphaBeta(chessboard, self.anfangtifet, -99999999, 99999999, self.color)
            #print(new_pos)
        else:
            new_pos = idx[0] # choose the only one position
            self.candidate_list.append((new_pos[0],new_pos[1]))
            if self.debug : print("No enough empty position")
        #===============Error handle===========================================
        # Make sure that the position in chess board is empty
        '''
        if not chessboard[new_pos[0],new_pos[1]]==0:
            new_pos = idx[len(idx)//2]         # replace with an empty position
            if self.debug : print("wrong")
        # Update decision into candidate_list
        if self.debug : print("Final position (%d, %d)"%(new_pos[0],new_pos[1]))
        if self.debug : print(chessboard)
        if self.debug : print()
        #self.candidate_list[-1]=((new_pos[0],new_pos[1]))
        self.candidate_list.append((new_pos[0],new_pos[1]))
        '''
        print(chessboard)
        #if self.debug :
        print("Final position (%d, %d)"%(self.candidate_list[-1][0], self.candidate_list[-1][1]))

    # Final search to get hightest score point
    def finalSearch(self, current_chessboard, chess_color, idx):
        added_chessboard = current_chessboard.copy() # H.F.: It may increase cost
        max_score_point = idx[0]
        max_score = -1000000000 # initial max_score
        #empty_points = np.where(added_chessboard == 0)
        empty_points = self.genNext(added_chessboard)
        #print(len(idx))
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
                    #if self.debug :
                    print("Score %d Point %s"%(score, empty_point))
                added_chessboard[empty_point[0], empty_point[1]] = 0
        else :
            #if self.debug: print("minMax")
            #start = time.time()

            for empty_point in empty_points:
                added_chessboard[empty_point[0], empty_point[1]] = chess_color
                score = self.alphaBeta(added_chessboard, 0, -99999999, 99999999, chess_color)
                #score = self.alphaBeta(added_chessboard, 1, max_score, 99999999, chess_color)
                #if self.debug: print("Final Score %d"%(score))
                #input("continue?")
                #print(added_chessboard)
                # from next
                if score > max_score:
                    max_score = score
                    max_score_point = empty_point
                    if self.debug : print("Score %d Point %s"%(score, empty_point))
                added_chessboard[empty_point[0], empty_point[1]] = 0
            #print("alphaBeta time cost: %d"%(time.time()-start))
        return max_score_point

    # Find out next position set
    def genNext(self, source_chessboard):
        #input("genNext?")
        #print(source_chessboard)
        pos = np.where(source_chessboard == 0)
        pos_package = list(zip(pos[0], pos[1]))
        # find positon with chess
        neighbor_points = []
        for chess in pos_package:
            for i, j in [(-1,-1), (-1,1), (1,-1), (1,1), (1,0), (0, 1),(-1,0),(0,-1)]:
                new_pos0 = chess[0]+i
                new_pos1 = chess[1]+j
                if new_pos0 > self.chessboard_size-1:
                    continue
                elif new_pos0 < 0 :
                    continue
                if new_pos1 > self.chessboard_size-1:
                    continue
                elif new_pos1 < 0:
                    continue
                if source_chessboard[new_pos0, new_pos1] != 0:
                    neighbor_points.append(chess)
                    break
        # sort the point return max point position
        '''
        for point in neighbor_points:
            x = point[0]
            y = point[1]
            if self.line5detect(source_chessboard, x, y):
                swap(neighbor_points[0], neighbor_points[neighbor_points.index(point)])
                break
            elif self.live4detect(source_chessboard,x,y):
                #print(neighbor_points[neighbor_points.index(point)])
                #swap(neighbor_points[-1], neighbor_points[neighbor_points.index(point)])
                break
            elif self.double3detect(source_chessboard, x,y):
                #swap(neighbor_points[1], neighbor_points[neighbor_points.index(point)])
                break
        '''
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
        return neighbor_points

    # alphabeta pruching
    def alphaBeta(self, source_chessboard, depth, alpha, beta, chess_color):
        #input("continue?")
        if depth == 0 : # or no empty position
            #print("final")
            if self.debug: print(source_chessboard)
            if self.debug: print(chess_color)
            #temp = self.evaluateState(source_chessboard, chess_color)
            temp= (self.evaluateState(source_chessboard, chess_color)
                -self.evaluateState(source_chessboard, -chess_color))
            #temp=temp*chess_color
            if self.debug: print("Now node score: %d"%(temp))
            return temp
        child_chessboard = source_chessboard.copy()
        candidate_points = self.genNext(child_chessboard)
        #print("Len: %d depth: %d"%(len(candidate_points), depth))
        max_wert = alpha
        max_point = candidate_points[0]
        for point in candidate_points :
            #print("search print %d %d"%(point[0], point[1]))
            child_chessboard[point[0], point[1]] = chess_color
            wert = -self.alphaBeta(child_chessboard, depth-1, -beta,-alpha, -chess_color)
            child_chessboard[point[0], point[1]] = 0
            #if self.debug :
            #print(depth, point, '->', wert)
            if wert > max_wert:
                max_wert = wert
                max_point = point
                if max_wert >= beta :
                    break
        if depth == self.anfangtifet :
            self.candidate_list.append(max_point)
            if self.debug: print("Final point: (%d, %d)"%(max_point[0], max_point[1]))
            #input()
        del child_chessboard
        #return beta # 对方最小得分
        #return chess_color*weight # 对方最小得分
        return max_wert

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
        jump = 0 # 跳
        # scan chess line to find style
        i = 0
        while(i<self.chessboard_size):
            if chess_line[i] == chess_color: # 找到己方棋子
                # 还原计算
                continue_point = 1
                block_point = 0
                # check left side if exit opponent's chess
                if chess_line[i-1] == -chess_color : block_point+=1
                # check linked chess
                i+=1
                while ((i<self.chessboard_size) and (chess_line[i] != -chess_color)):
                    if chess_line[i] == 0 and chess_line[i+1]==chess_color :
                        jump +=1 # 暂时忽略跳子
                    elif chess_line[i] == chess_color:
                        continue_point+=1
                    else:
                        i+=1
                        break
                    i+=1
                if chess_line[i] == -chess_color: block_point+=1 # 边界也算冲
                #print("Label%d %d"%(continue_point, block_point))
                linevalue += self.mapValue(continue_point, block_point, jump)
            i+=1
        return linevalue

    # maping score from chess style
    def mapValue(self, continue_point, block_point, jump):
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
        else: # both two side are opponent's chess
            #print("死")
            if continue_point>= 5: return score_map['LINEFIVE']
            else: return score_map['DEADZERO']

    def line5detect(self, chessboard, x, y):
        #print("Detect line5 on (%d, %d)"%(x, y))
        result = 0
        for i in range(-4,5): # Todo: this range is over
            if x+i>-1 and x+i+4<self.chessboard_size : # check in horizontal
                #print("Searching in horizontal (%d, %d)"%(y,x+i))
                temp_x = self.color*sum(chessboard[y,x+i:x+i+4])
                if temp_x == 4 :
                    result = 1
                    break
                elif temp_x == -4 :
                    result = 1
                    print("Found opponent's horizontal line5 in %d"%(y))
            if y+i>-1 and y+i+4<self.chessboard_size :      # check in vertical
                temp_y = self.color*sum(chessboard[y+i:y+i+4,x])
                if temp_y == 4 :
                    result = 1
                    print("Found our vertical line5 in %d"%(x))
                    break
                elif temp_y == -4:
                    print("Found opponent's vertical line5 in %d"%(x))
                    result = 1
                if x+i>-1 and x+i+4<self.chessboard_size :  # check in diagonal
                    temp_sum = 0
                    for j in range (0,5):
                        temp_sum += chessboard[y+i+j, x+i+j]
                    temp_d = self.color*temp_sum
                    if temp_d == 4:
                        result = 1
                        print("Found our Line5 diagonal")
                        break
                    elif temp_d == -4:
                        result = 1
                        print("Found opponent line5 diagonal")
        return result

    def live4detect(self, chessboard, x, y):
        result = 0
        pattern = self.color*np.array([0,1,1,1,1,0])
        #print("Checking point live4 (%d, %d)"%(x,y))
        temp_y = 0
        temp_x = 0
        temp_d = 0 # in diagose
        for i in range(-3,1):
            if (x+i-1 > -1) and (x+i+4 < self.chessboard_size) : # in horizontal
                temp_x = np.dot(pattern, chessboard[y, x+i-1:x+i+5])
                #print("Check live4 in horizon %s"%(chessboard[y,x+i-1:x+i+5]))
            if (y+i-1 > -1) and (y+i+4 < self.chessboard_size) : # in vertical
                temp_y = np.dot(pattern, chessboard[y+i-1:y+i+5, x])
                array_d = np.zeros(6)
                if(x+i-1 > -1) and (x+i+4 < self.chessboard_size) : # in diag
                    for j in range(0,6):
                        #print( chessboard[y+i-1+j, x+i-1+j])
                        array_d[j]=chessboard[y+i-1+j, x+i-1+j]
                    temp_d = np.dot(array_d, pattern)
            #print("temp_x:%d"%(temp_x))
            if (temp_x == 3) or (temp_y == 3) or (temp_d == 3):
                print("Biuld live4!(%d, %d)"%(x,y))
                result = 1
                #self.live4_flag = 1                # mark for next step
                break
            elif (temp_x == -3) or (temp_y == -3) or (temp_d == -3):
                #print("Found oppoent's live4 on (%d, %d)"%(x,y))
                result = 1
        return result

    def double3detect(self, chessboard, x, y):
        #print("Double3 detecting on (%d, %d)"%(x, y))
        result = 0
        temp_x1 = 0
        temp_x2 = 0
        temp_y1 = 0
        temp_y2 = 0
        pattern = self.color*np.array([0,1,1,0])
        # in horizontal
        if x-3 > -1 :
            #print(chessboard[y, x-3:x+1])
            temp_x1 = np.dot(pattern, chessboard[y, x-3:x+1])
        elif x+4 < self.chessboard_size :
            #print(chessboard[y, x:x+4])
            temp_x2 = np.dot(pattern, chessboard[y, x:x+4])
        # in vectical
        if y-3 > -1 :
            temp_y1 = np.dot(pattern, chessboard[y-3:y+1, x])
        elif y+4 < self.chessboard_size :
            temp_y2 = np.dot(pattern, chessboard[y:y+4, x])
        # combine horizontal and vectical
        if (temp_x1 == 2 or temp_x2 == 2) and (temp_y1==2 or temp_y2==2):
            print("Found our double3 (%d, %d)"%(x, y))
            result = 1
        elif (temp_x1 == -2 or temp_x2 == -2) and (temp_y1==-2 or temp_y2==-2):
            result = 1
            print("Found opponent's double3 (%d, %d)"%(x, y))
        return result

