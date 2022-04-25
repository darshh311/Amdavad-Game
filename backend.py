import numpy as np

dice = np.array([1, 2, 3, 4, 8])
def getdicevalue():
    return np.random.choice(dice[:])





def heuristic(i, dicenumber, opponent, paths, jiskaturn):
    E = 1
    temp = paths.index(jiskaturn[i])
    distancefromgoal = len(paths) - temp

    temp = temp + dicenumber
    if temp >= len(paths):
        return 0
    tempvalue = paths[temp]
    if temp == 4 or temp==8 or temp==12 or temp==len(paths)-1:
        E+=8
    elif tempvalue in opponent:
        E+=10
    else:
        E+=8
    
    temp = paths.index(jiskaturn[i])
    tempvalue = paths[temp]
    steps=1
    temp = temp-1
    while steps<=9 and temp>=0:
        tempvalue = paths[temp]
        if tempvalue in opponent:
            break
        else:
            steps = steps+1
            temp = temp-1
    
    if steps > 8:
        E+=6
    elif steps > 4:
        E+=5
    elif steps > 3:
        E+=4
    elif steps > 2:
        E+=3
    elif steps > 1:
        E+=2
    else:
        E+=1
    
    temp = paths.index(jiskaturn[i])
    steps=0
    if(temp<4):
        steps = 4 - temp
    elif(temp<8):
        steps = 8 - temp
    elif(temp<12):
        steps = 12 - temp
    elif(temp<25):
        steps = 25 - temp
    elif temp==4 or temp==8 or temp==12:
        steps = 99999
    elif temp==len(paths)-1:
        steps = math.inf
    


    E = E/float(steps + distancefromgoal)

    return E


pathofred = [[0,2], [0,1], [0,0], [1,0], [2,0], [3,0], [4,0], [4,1], [4,2], [4,3], [4,4], [3,4], [2,4], [1,4], [0,4], [0,3], [1,3], 
             [2,3], [3,3], [3,2], [3,1], [2,1], [1,1], [1,2], [2,2]]
pathofblue = [[4,2], [4,3], [4,4], [3,4], [2,4], [1,4], [0,4], [0,3], [0,2], [0,1], [0,0], [1,0], [2,0], [3,0], [4,0], [4,1], [3,1], 
              [2,1], [1,1], [1,2], [1,3], [2,3], [3,3], [3,2], [2,2]]

red = [[0,2], [0,2], [0,2], [0,2]]
blue = [[4,2], [4,2], [4,2], [4,2]]

safehouse = [(0,2), (2,0), (4,2), (2,4), (2,2)]

matrixofred = np.array( [[0,0,4,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]] )

matrixofblue = np.array ( [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,4,0,0]] )




gameon = True
turn = 0
while gameon:
    if matrixofred[2][2] == 4 or matrixofblue[2][2]==4:
        gameon = False
        break
    
    if turn == 0:
        dicevalue = getdicevalue()
        print(dicevalue)
        eval = 0
        pawn = 0
        for i in range(len(red)):
            evaluation = heuristic(i, dicevalue, blue, pathofred, red)
            if(eval<evaluation):
                eval = evaluation
                pawn = i
        flag = 0
        prevpos = red[pawn]
        if pathofred.index(prevpos)+dicevalue<len(pathofred):
            matrixofred[red[pawn][0]][red[pawn][1]] -= 1
            red[pawn] = pathofred[pathofred.index(prevpos)+dicevalue]
            matrixofred[red[pawn][0]][red[pawn][1]] += 1
            flag = 1
        #print("r")
        #print(red)
        turn = 1
        if pathofred.index(red[pawn]) == 4 or pathofred.index(red[pawn]) == 8 or pathofred.index(red[pawn]) == 12 or pathofred.index(red[pawn]) == len(pathofred)-1:
            turn = 1
        else:
            if (red[pawn] in blue) and flag==1:
                matrixofblue[blue[blue.index(red[pawn])][0]][blue[blue.index(red[pawn])][1]] -= 1
                ind = blue.index(red[pawn])
                blue[ind][0] = 4
                blue[ind][1] = 2
                matrixofblue[4][2] += 1
                turn = 0
        
        
    else:
        dicevalue = getdicevalue()
        print(dicevalue)
        eval = 0
        pawn = 0
        for i in range(len(blue)):
            evaluation = heuristic(i, dicevalue, red, pathofblue, blue)
            if(eval<evaluation):
                eval = evaluation
                pawn = i
        prevpos = blue[pawn]
        flag = 0
        if pathofblue.index(prevpos)+dicevalue<len(pathofblue):
            matrixofblue[blue[pawn][0]][blue[pawn][1]] -= 1
            blue[pawn] = pathofblue[pathofblue.index(prevpos)+dicevalue]
            matrixofblue[blue[pawn][0]][blue[pawn][1]] += 1
            flag = 1
        #print("b")
        #print(blue)
        turn = 0
        if pathofblue.index(blue[pawn]) == 4 or pathofblue.index(blue[pawn]) == 8 or pathofblue.index(blue[pawn]) == 12 or pathofblue.index(blue[pawn]) == len(pathofblue)-1:
            turn = 0

        else:
            if (blue[pawn] in red) and flag == 1:
                matrixofred[red[red.index(blue[pawn])][0]][red[red.index(blue[pawn])][1]] -= 1
                ind = red.index(blue[pawn])
                red[ind][0] = 0
                red[ind][1] = 2
                matrixofred[0][2] += 1
                turn = 1
        
        
        
    
    print(matrixofred)
    print(matrixofblue)
    
    
    
    