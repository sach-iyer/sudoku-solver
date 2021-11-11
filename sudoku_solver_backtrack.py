# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:36:27 2020

@author: sachi
"""
#   All coordinates are in form (row,column)

#   All functions return : (Functions with only  2 output states return either 0 or 1)
    #   0  if invalid (eg, two  '9' in same row).
    #   2  if valid but not complete (ie. empty boxes might be present).
    #   1  if valid and complete (all 9 nos present).

#   df_sudo holds solution;
#   df_sudo_question holds question for backtracking;
#   df_sudo_orig_question remains unchanged

# INFO: if (-1): returns a True

    

import numpy as np
import pandas  as pd

########################## GLOBAL VARIABLES ##########################

path_to_question = r""
output_excel = r""

df_sudo_question = pd.read_excel(path_to_question, sheet_name='io', usecols='A:J', header=0, index_col=0, skiprows=range(2), nrows=9)

# Converting NaN values (if they exist) to zero
for i in range(9):
    for j in range(9):
        if df_sudo_question.loc[i,j] not in range(10):
            df_sudo_question.loc[i,j] = 0
            
# Converting data type of all values to int (from numpy.float64) 
df_sudo_question = df_sudo_question.astype(int)
df_sudo = df_sudo_question.copy()
df_sudo_orig_question = df_sudo_question.copy()

############################  FUNCTIONS   ###########################
            
def box_of_cell(cell):
    return (int(cell[0]/3),int(cell[1]/3))    

def is_all9(count_nos):
    
        if (count_nos.count(0)+count_nos.count(1)) == 9:
            if (count_nos.count(1)) == 9:
                return 1
            return 2
        return 0

def next_cell(cell):
    cell = list(cell)
    while(1):
        if cell[1]>=8:
            if cell[0]>=8:
                return 0
            else:
                cell[1]=0
                cell[0]+=1
        else:
            cell[1]+=1
        
        if df_sudo_question.loc[cell[0],cell[1]] == 0:
            return tuple(cell)
        
def prev_cell(cell):
    cell = list(cell)
    while(1):
        if cell[1]<=0:
            if cell[0]<=0:
                return 0
            else:
                cell[1]=8
                cell[0]-=1
        else:
            cell[1]-=1
        
        if df_sudo_question.loc[cell[0],cell[1]] == 0:
            return tuple(cell)
            

def solve_backtrack():
    global df_sudo          #Change your mind?
    cell = (0,0)
    is_change_made = 1              #Flag variable
    if df_sudo_question.loc[cell[0],cell[1]] != 0:
        cell = next_cell(cell)
        
    while(1):
#        print(cell)             #Test
#        print(df_sudo)          ##########  Big test ---------------------
        if is_change_made:
            old_num = df_sudo.loc[cell[0],cell[1]]
            is_change_made=0
        
        if old_num==9:                          #Backtrack?
            df_sudo.loc[cell[0],cell[1]] = 0
            cell = prev_cell(cell)
            
            if cell==0:
                print("Failed")
                print(df_sudo)
                return 0
            is_change_made=1
            continue
        
        new_num=old_num+1
        if nos_in_row(df_sudo, cell[0])[new_num-1]==0:
            if nos_in_col(df_sudo, cell[1])[new_num-1]==0:
                if nos_in_box(df_sudo, box_of_cell(cell))[new_num-1]==0:
                    df_sudo.loc[cell[0],cell[1]] = new_num
                    cell = next_cell(cell)
                    if cell==0:
                            print("Solved?")    #check if  sudo valid
                            return 1
                        
                    is_change_made=1
                    continue
        
        # if it fails any of the above if statements:
        old_num = new_num
#        if cell[1]==8:                  #FOR TESTING
#            print(cell)
        pass
    pass
    

def is_sudo_valid(sudoku):
    pass

def is_cell_valid(sudoku, cell): #To bo modified #Do I even need this??
    
    r=is_all9(nos_in_row(df_sudo, cell[0]))
    c=is_all9(nos_in_col(df_sudo, cell[1]))
    b=is_all9(nos_in_box(df_sudo, box_of_cell(cell)))
    
    print(r,c,b)    #Testing
    
    if r and c and b:
        return 1                    # Returns only 1 or 0 as no possible 3rd state
    
    return 0

def nos_in_row(sudoku, row):
    count_nos = [0,0,0,0,0,0,0,0,0]
    
    for i in range(9):
        n = sudoku.loc[row,i]
        if n:
            count_nos[n-1]+=1
    
#    print(count_nos)
            
    return count_nos
    
def nos_in_col(sudoku, col):
    count_nos = [0,0,0,0,0,0,0,0,0]
    
    for i in range(9):
        n = sudoku.loc[i,col]
        if n:
            count_nos[n-1]+=1
            
    return count_nos


def nos_in_box(sudoku, box):
    
    count_nos = [0,0,0,0,0,0,0,0,0]
    
    for i in range(3*box[0],3*box[0]+3):
        for j in range(3*box[1],3*box[1]+3):
            n = sudoku.loc[i,j]
            if n:
                count_nos[n-1]+=1

    return count_nos




def solve():
    
    import time
    start_time=time.time()
    
    solve_backtrack()                              
    df_sudo.to_excel(output_excel)
    
    print ('Time Taken(s):',time.time()-start_time())

solve()

###########################################################

#   Archive:
    
"""
def is_lines_valid(sudoku, cell):
    count_nos1 = [0,0,0,0,0,0,0,0,0]
    count_nos2 = count_nos1
    
    for i in range(9):
        n = sudoku.loc(i,cell[1])
        if n:
            count_nos1[n-1]+=1


    for i in range(9):
        n = sudoku.loc(cell[0],i)
        if n:
            count_nos2[n-1]+=1
            
        if (count_nos1.count(0)+count_nos1.count(1)) == (count_nos2.count(0)+count_nos2.count(1))==9:
            if (count_nos1.count(1)==count_nos2.count(1)==9):
                return
"""

##############################################################
"""
def to_set(count_nos):
    set_nos = {}
    for i in range(9):
        if (count_nos[i]):
            set_nos.add(i+1)
    return set_nos


def reduce_rows(sudoku, pencil):
    
    for i in range(9):
        nos = to_set(nos_in_row(sudoku, i))
        for j in range(9):
            pencil[(i,j)].add
            

            
        
        


def solve_logically():
    global df_sudo, df_sudo_question

    pencil = dict()
    
    for i in range(9):
        for j in range(9):
            if df_sudo_question.loc[i,j] ==0:
                pencil[(i,j)] = set(range(1,10))
            
            else:
                
    
    """
#############################################################