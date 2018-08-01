
from itertools import chain


__builtins__.Z3_LIB_DIRS = ['/home/workspace/z3/bin']
from z3 import *

#This Program uses a SAT solver(Z3) to solve a 3d Sudoku Problem
#This is the solution to a constraint satisfaction problem



# Top Face
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# -----------------
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0

# Left Face
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# -----------------
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0


# Right Face
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# -----------------
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0
# 0 0 0 0 | 0 0 0 0

# Three faces connected as a cub


msolver = Solver()

# Naming Boxes for Solver
rows = 'A B C D E F G H I J K L M N O P'.split()
cols = ['{}'.format(i+1) for i in range(16)]
boxes = [[Int('{}{}'.format(r,c)) for c in cols] for r in rows]
boxes_transpose = [[Int("{}{}".format(r,c)) for r in rows] for c in cols]
top = []
left = []
right = []

for x in boxes[:8]:
    top.append(x[:8])
    
for i in boxes_transpose[8:]:
    for j in [i[:8]]:
        right.append(j[::-1])
for x in boxes[8:]:
    left.append(x[:8])
    
# Toget is a dictionary with all the boxes together based on face of cube
toget = {}
toget['top'] = top
toget['left'] = left
toget['right'] = right


c1 = ['1 2 3 4', '5 6 7 8']
c2 = ['9 10 11 12', '13 14 15 16']
r1 = ['A B C D', 'E F G H']
r2 = ['I J K L', 'M N O P']


# All the squares in the cube 
squares=[]
for i in r1:
    for j in c1:
        squares.append([k+l for k in i.split() for l in j.split()])

for i in r2:
    for j in c1:
        squares.append([k+l for k in i.split() for l in j.split()])
        
for i in r1:
    for j in c2:
        squares.append([k+l for k in i.split() for l in j.split()])

# all of the squares throughout the cube
boxes_squares = [[Int("{}".format(box)) for  box in square] for square in squares]

#top-face to right-face units(units meaning row or column or small/)
tr = []
for x in boxes[:8]:
    tr.append(x)

#top-face to left-face units
tl = []
for x in boxes_transpose[:8]:
    tl.append(x)

#left-face to right-face units   
lr=[]
for i in boxes[8:]:
    for j in [i[:8]]:
        lr.append(j)
        
for i in boxes_transpose[8:]:
    for j in [i[:8]]:
        lr.append(j[::-1])
        
for i, j in enumerate(lr[:8]):
    lr[i] = lr[i]+lr[i+8]
    
lr = lr[:8]


all_rows = list((tr,tl,lr))



# Constaints

# 3-d Sudoku Specific Constraint: All rows and columns must be between 1-16
msolver.add(*chain(*[(0< box, box <=16) for box in chain(*chain(*toget.values()))]))

# Constraint for distinct values 1-16
msolver.add([Distinct(row) for row in [*chain(*all_rows)]])
msolver.add([Distinct(x) for x in boxes_squares])



# 0 represents missing square
# Filled in is inital conditions
board = {
    'top':
    [(0,8,0,1,0,0,0,0),
    (0,2,13,0,0,10,16,0),
    (4,5,6,0,1,8,9,0),
    (0,0,10,14,0,6,0,5),
    (8,13,0,0,3,7,0,15),
    (9,0,7,0,0,16,0,6),
    (6,0,0,5,0,0,0,8),
    (0,15,0,0,0,13,0,2)],
    
    'left':
    [(0,1,0,7,6,2,0,0),
    (0,0,0,0,15,1,11,0),
    (2,0,0,0,13,0,0,0),
    (10,9,8,13,0,14,0,0),
    (0,4,0,0,2,0,0,12),
    (7,0,0,0,16,0,10,1),
    (0,0,5,9,14,0,15,0),
    (0,14,0,6,0,5,0,0)],
    
    'right':
    [(0,13,0,14,16,0,11,0),
    (9,0,0,0,0,13,14,0),
    (12,16,0,0,9,0,8,0),
    (6,0,2,0,0,7,0,0),
    (0,11,0,0,1,0,0,16),
    (0,0,0,0,15,2,0,13),
    (0,0,13,16,0,0,0,10),
    (0,0,15,1,0,0,0,4)],
}

# Constraint for solver to know that if the board has a value other then zero, dont change it
for key in toget.keys():
    msolver.add([toget[key][i][j] == board[key][i][j] for i in range(8) for j in range(8) if board[key][i][j]!=0])
    


assert msolver.check() == sat, "Uh oh. The solver didn't find a solution"
for key in toget.keys():
    for row, _boxes in enumerate(toget[key]):
        if row and row % 4 == 0:
            print('-'*9+'-'*9+'-'*9)
        for col, box in enumerate(_boxes):
            if col and col % 4 == 0:
                print('|', end='')
            print(' {} '.format(msolver.model()[box]), end='')  # Solver models a solution



# Solution

# Top Face
# 11  8  9  1 | 7  15  2  14 
#  12  2  13  15 | 4  10  16  3 
#  4  5  6  16 | 1  8  9  11 
#  3  7  10  14 | 12  6  13  5 
# ---------------------------
#  8  13  12  2 | 3  7  5  15 
#  9  11  7  4 | 10  16  14  6 
#  6  10  1  5 | 9  12  4  8 
#  14  15  16  3 | 11  13  1  2 


# Left Face
#  15  1  4  7 | 6  2  8  9 
#  5  16  3  12 | 15  1  11  10 
#  2  6  14  11 | 13  4  3  7 
#  10  9  8  13 | 5  14  12  16 
# ---------------------------
#  13  4  15  10 | 2  3  6  12 
#  7  3  11  8 | 16  9  10  1 
#  1  12  5  9 | 14  11  15  4 
#  16  14  2  6 | 8  5  7  13 


# Right Face
#  5  13  3  14 | 16  10  11  12 
#  9  7  8  4 | 2  13  14  6 
#  12  16  1  10 | 9  15  8  5 
#  6  15  2  11 | 4  7  1  3 
# ---------------------------
#  8  11  5  9 | 1  14  7  16 
#  4  14  12  6 | 15  2  5  13 
#  7  2  13  16 | 8  3  6  10 
#  10  3  15  1 | 11  12  9  4 
    