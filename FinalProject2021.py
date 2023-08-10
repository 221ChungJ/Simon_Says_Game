import random
import sys
import time
import pygame
from collections import deque

def drawButtons():
    pygame.draw.rect(DisplayScreen, Red,    RedRect)
    pygame.draw.rect(DisplayScreen, Green,  GreenRect)
    pygame.draw.rect(DisplayScreen, Blue,   BlueRect)
    pygame.draw.rect(DisplayScreen, Yellow, YellowRect)

def checkQuit():
    for event in pygame.event.get(pygame.QUIT): 
        pygame.quit()
        sys.exit()

def flashAnimation(color, animationSpeed=50):
    flashColor = None
    rectangle = None
    if color == Red:
        flashColor = BrightRed
        rectangle = RedRect
    elif color == Blue:
        flashColor = BrightBlue
        rectangle = BlueRect
    elif color == Green:
        flashColor = BrightGreen
        rectangle = GreenRect
    elif color == Yellow:
        flashColor = BrightYellow
        rectangle = YellowRect

    origScreen = DisplayScreen.copy()
    flashScreen = pygame.Surface((300, 300))
    flashScreen = flashScreen.convert_alpha()
    r, g, b = flashColor
    for start, end, step in ((0, 255, 1), (255, 0, -1)): 
        for alpha in range(start, end, animationSpeed * step):
            checkQuit()
            DisplayScreen.blit(origScreen, (0, 0))
            flashScreen.fill((r, g, b, alpha))
            DisplayScreen.blit(flashScreen, rectangle.topleft)
            pygame.display.update()
            FPSClock.tick(FPS)
    DisplayScreen.blit(origScreen, (0, 0))

def checkButtonClicked(x, y):
    if RedRect.collidepoint((x, y)):
        return Red
    elif BlueRect.collidepoint((x, y)):
        return Blue
    elif GreenRect.collidepoint((x, y)):
        return Green
    elif YellowRect.collidepoint((x, y)):
        return Yellow
    return None
    

# Colors
White = (255, 255, 255)
Gray = (80, 80, 80)
Black = (0,0,0)
BrightRed = (255, 0, 0)
Red = (155, 0, 0)
BrightGreen = (0, 255, 0)
Green = (0, 155, 0)
BrightBlue = (0, 0, 255)
Blue = (0, 0, 155)
BrightYellow = (255, 255, 0)
Yellow = (155, 155, 0)

pygame.init()
FPS = 30
FPSClock = pygame.time.Clock()

# Screen Creation
DisplayWidth = 960
DisplayHeight = 720
DisplayScreen = pygame.display.set_mode((DisplayWidth, DisplayHeight))
pygame.display.set_caption("Simon Says")


# Game Setup
font1 = pygame.font.SysFont("calibri",24)
instructionsObj = font1.render("Match the pattern by clicking on the colored squares in the order they are flashed in", 1, Gray)
instructionsRect =  instructionsObj.get_rect()
instructionsRect.center = (DisplayWidth/2, DisplayHeight-25)

# Button Creation
RedRect = pygame.Rect(0, 0, 300, 300)
GreenRect = pygame.Rect(0, 0, 300, 300)
BlueRect = pygame.Rect(0, 0, 300, 300)
YellowRect = pygame.Rect(0,0, 300, 300)
GreenRect.center = (320, 200)
RedRect.center = (640, 200)
YellowRect.center = (320,520)
BlueRect.center = (640,520)

score = 0

queue = deque()

CheckButtonInput = True

# Game Loop
while True:
    clickedButton = None
    DisplayScreen.fill(Black)
    drawButtons()

    # Creates score text
    font2 = pygame.font.SysFont("impact",32)
    scoreObj = font2.render("Score: " + str(score), 1, White)
    scoreRect = scoreObj.get_rect()
    scoreRect.center = (DisplayWidth/2, DisplayHeight-695)
    
    # Displays the text
    DisplayScreen.blit(scoreObj, scoreRect)
    DisplayScreen.blit(instructionsObj, instructionsRect)
    
    # Checks if the player has exited the program
    checkQuit()

    # Checks what button is clicked
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and CheckButtonInput:
            xPos, yPos = event.pos
            clickedButton = checkButtonClicked(xPos, yPos)
    
    # Checks to see if the player has clicked all the squares in the correct order
    # If the player clicks all the squares in the correct order, it creates a new pattern, increasing the pattern by 1 each time
    if len(queue) == 0:
        pygame.display.update()
        pygame.time.wait(1000)
        CheckButtonInput = False
        for i in range(score+1):
            colorSelected = random.choice((Red, Blue, Green, Yellow))
            queue.append(colorSelected)
            flashAnimation(colorSelected)
            pygame.time.wait(200)
        CheckButtonInput = True
    else:
        correctColor = queue[0]
        if clickedButton != None and correctColor == clickedButton:
            flashAnimation(correctColor)
            queue.popleft()
            if len(queue) == 0:
                score += 1
        # If the player does not click the squares in the correct order, the game over screen appears and the game restarts after 5 seconds
        elif clickedButton != None and correctColor != clickedButton:
            DisplayScreen.fill((139, 0, 0))
            font3 = pygame.font.SysFont("impact",64)
            gameoverObj = font3.render("GAME OVER", 1, Black)
            gameoverRect = gameoverObj.get_rect()
            gameoverRect.center = (DisplayWidth/2, DisplayHeight/2)
            font4 = pygame.font.SysFont("impact",32)
            endScoreObj = font4.render("Score: " + str(score), 1, Black)
            endScoreRect = endScoreObj.get_rect()
            endScoreRect.center = (DisplayWidth/2, DisplayHeight/2+64)
            DisplayScreen.blit(endScoreObj, endScoreRect)
            DisplayScreen.blit(gameoverObj, gameoverRect)
            pygame.display.update()
            pygame.time.wait(5000)
            queue.clear()
            score = 0

    pygame.display.update()
    FPSClock.tick(FPS)




