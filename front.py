import pygame, sys
import time

pygame.init()


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





def gameon(turn):
    
    
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
    
    
    
    
















width = 1000
height = 1000
bg_color = (28,170,156)
screen = pygame.display.set_mode((width,height))

pygame.display.set_caption( 'Amdavad' )

screen.fill(bg_color)
line_color = (23, 145, 135)
line_width = 15

def draw_lines():
    pygame.draw.line(screen, line_color, (0, 200), (1000, 200), line_width)
    pygame.draw.line(screen, line_color, (0, 400), (1000, 400), line_width)
    pygame.draw.line(screen, line_color, (0, 600), (1000, 600), line_width)
    pygame.draw.line(screen, line_color, (0, 800), (1000, 800), line_width)
    pygame.draw.line(screen, line_color, (200, 0), (200, 1000), line_width)
    pygame.draw.line(screen, line_color, (400, 0), (400, 1000), line_width)
    pygame.draw.line(screen, line_color, (600, 0), (600, 1000), line_width)
    pygame.draw.line(screen, line_color, (800, 0), (800, 1000), line_width)
    pygame.draw.line(screen, line_color, (200, 400), (0, 600), line_width)
    pygame.draw.line(screen, line_color, (0, 400), (200, 600), line_width)
    pygame.draw.line(screen, line_color, (400, 0), (600, 200), line_width)
    pygame.draw.line(screen, line_color, (400, 200), (600, 0), line_width)
    pygame.draw.line(screen, line_color, (400, 400), (600, 600), line_width)
    pygame.draw.line(screen, line_color, (600, 400), (400, 600), line_width)
    pygame.draw.line(screen, line_color, (400, 1000), (600, 800), line_width)
    pygame.draw.line(screen, line_color, (600, 1000), (400, 800), line_width)
    pygame.draw.line(screen, line_color, (800, 400), (1000, 600), line_width)
    pygame.draw.line(screen, line_color, (1000, 400), (800, 600), line_width)
    
draw_lines()
dic = { 0:80 , 1:280 , 2:480 , 3:680 , 4:880 }
swidth = 40
sheight = 40
rx1 = 480
ry1 = 40
rx2 = 480
ry2 = 120
rx3 = 440
ry3 = 80
rx4 = 520
ry4 = 80
bx1 = 480
by1 = 840
bx2 = 480
by2 = 920
bx3 = 440
by3 = 880
bx4 = 520
by4 = 880

def draw_box():
    pygame.draw.rect(screen, (255, 0, 0), (rx1, ry1, swidth, sheight))
    pygame.draw.rect(screen, (255, 0, 0), (rx2, ry2, swidth, sheight))
    pygame.draw.rect(screen, (255, 0, 0), (rx3, ry3, swidth, sheight))
    pygame.draw.rect(screen, (255, 0, 0), (rx4, ry4, swidth, sheight))
    pygame.draw.rect(screen, (0, 255, 0), (bx1, by1, swidth, sheight))
    pygame.draw.rect(screen, (0, 255, 0), (bx2, by2, swidth, sheight))
    pygame.draw.rect(screen, (0, 255, 0), (bx3, by3, swidth, sheight))
    pygame.draw.rect(screen, (0, 255, 0), (bx4, by4, swidth, sheight))
    
draw_box()

gameoned = True
turn = 0
while gameoned:
    if matrixofred[2][2] == 4 or matrixofblue[2][2]==4:
        gameoned = False
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
    
    pygame.display.update()


    screen.fill(bg_color)
    draw_lines()

    rx1 = dic[red[0][0]]
    ry1 = dic[red[0][1]]
    rx2 = dic[red[1][0]]
    ry2 = dic[red[1][1]]
    rx3 = dic[red[2][0]]
    ry3 = dic[red[2][1]]
    rx4 = dic[red[3][0]]
    ry4 = dic[red[3][1]]
    bx1 = dic[blue[0][0]]
    by1 = dic[blue[0][1]]
    bx2 = dic[blue[1][0]]
    by2 = dic[blue[1][1]]
    bx3 = dic[blue[2][0]]
    by3 = dic[blue[2][1]]
    bx4 = dic[blue[3][0]]
    by4 = dic[blue[3][1]]

    draw_box()
    
    time.sleep(0.25)
    

    print(matrixofred)
    print(matrixofblue)
    
    
    
    

turn = 0
while False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    gameplaying = True
    while gameplaying:
        if matrixofred[2][2] == 4 or matrixofblue[2][2]==4:
            gameplaying = False
            break
        gameon(turn)
        pygame.draw.rect(screen, (255, 0, 0), (rx1, ry1, swidth, sheight))
        pygame.draw.rect(screen, (255, 0, 0), (rx2, ry2, swidth, sheight))
        pygame.draw.rect(screen, (255, 0, 0), (rx3, ry3, swidth, sheight))
        pygame.draw.rect(screen, (255, 0, 0), (rx4, ry4, swidth, sheight))
        pygame.draw.rect(screen, (0, 255, 0), (bx1, by1, swidth, sheight))
        pygame.draw.rect(screen, (0, 255, 0), (bx2, by2, swidth, sheight))
        pygame.draw.rect(screen, (0, 255, 0), (bx3, by3, swidth, sheight))
        pygame.draw.rect(screen, (0, 255, 0), (bx4, by4, swidth, sheight))

        rx1 = dic[red[0][0]]
        ry1 = dic[red[0][1]]
        rx2 = dic[red[1][0]]
        ry2 = dic[red[1][1]]
        rx3 = dic[red[2][0]]
        ry3 = dic[red[2][1]]
        rx4 = dic[red[3][0]]
        ry4 = dic[red[3][1]]
        bx1 = dic[blue[0][0]]
        by1 = dic[blue[0][1]]
        bx2 = dic[blue[1][0]]
        by2 = dic[blue[1][1]]
        bx3 = dic[blue[2][0]]
        by3 = dic[blue[2][1]]
        bx4 = dic[blue[3][0]]
        by4 = dic[blue[3][1]]

        
        pygame.display.update()
        time.sleep(1)