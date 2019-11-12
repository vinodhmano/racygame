import pygame
import time
import random

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_RED = (200,0,0)
LIGHT_GREEN = (0,200,0)

carImage = pygame.image.load('car.png')
car_width = 55

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Racy Game')
clock = pygame.time.Clock()


#all methods

def paintScore(count):
    font = pygame.font.SysFont(None,25)
    text = font.render('Dodged : ' + str(count), True, BLUE)
    gameDisplay.blit(text,(0,0))


def text_objects(text, font, color):
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()


def display_message(text):
    font = pygame.font.Font('freesansbold.ttf',100)
    message_surface, message_rect = text_objects(text, font, RED)
    message_rect.center = ((DISPLAY_WIDTH/2),(DISPLAY_HEIGHT/2))
    gameDisplay.blit(message_surface,message_rect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def crashed():
    display_message('You Crashed')


def quitgame():
    pygame.quit()

def car(x,y):
    gameDisplay.blit(carImage,(x,y))


def enemy(x,y,enemy_width, enemy_height, enemy_color):
    pygame.draw.rect(gameDisplay,enemy_color,[x,y,enemy_width, enemy_height])


def button(text, button_x, button_y, button_width, button_height, hover_color, default_color, action=None):
     #mouse tracker in the form of (x,y) tuple
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if (button_x + button_width) > mouse[0] > button_x and (button_y + button_height) > mouse[1] > button_y:
            pygame.draw.rect(gameDisplay,hover_color,(button_x, button_y, button_width, button_height))
            if click[0] == 1 and action != None:
                action()
    else:
        pygame.draw.rect(gameDisplay,default_color,(button_x, button_y, button_width, button_height))

    font = pygame.font.Font('freesansbold.ttf',20)
    button_text_surface, button_text_rect = text_objects(text,font,BLACK)
    button_text_rect.center = (button_x + (button_width/2), button_y + (button_height/2))
    gameDisplay.blit(button_text_surface, button_text_rect)


def intro():
    button_width = 100
    button_height = 50
    start_button_x = DISPLAY_WIDTH/10
    start_button_y = DISPLAY_HEIGHT/2
    quit_button_x = DISPLAY_WIDTH/1.3
    quit_button_y = DISPLAY_HEIGHT/2

    gameDisplay.fill(WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
       
        
        #display the Welcome message
        font = pygame.font.Font('freesansbold.ttf',50)
        intro_message_surface, intro_message_rect = text_objects('WELCOME TO THE GAME',font,BLACK)
        intro_message_rect.center = ((DISPLAY_WIDTH/2),(DISPLAY_HEIGHT/4))
        gameDisplay.blit(intro_message_surface, intro_message_rect)

        #display the buttons
        #pygame.draw.rect(gameDisplay,LIGHT_GREEN,(start_button_x, start_button_y, button_width, button_height))
        #pygame.draw.rect(gameDisplay,LIGHT_RED, (quit_button_x, quit_button_y, button_width, button_height))

        button('Play',start_button_x,start_button_y,button_width,button_height,LIGHT_GREEN,GREEN,game_loop)
        button('Quit',quit_button_x,quit_button_y,button_width,button_height,LIGHT_RED,RED,quitgame)
        
        
        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = DISPLAY_WIDTH * .45
    y = DISPLAY_HEIGHT * .9
    x_change = 0
    y_change = 0

    enemy_x = random.randrange(0,DISPLAY_WIDTH)
    enemy_y = -600
    enemy_speed = 7
    enemy_width = 100
    enemy_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or pygame.K_DOWN:
                    y_change = 0

        x += x_change
        y += y_change

        gameDisplay.fill(WHITE)
        car(x,y)    
        enemy(enemy_x,enemy_y,enemy_width,enemy_height,RED)
        enemy_y += enemy_speed
        paintScore(dodged)

        if x > DISPLAY_WIDTH - car_width or x < 0:
            crashed()
        
        if enemy_y > DISPLAY_HEIGHT:
            enemy_y = 0 - enemy_y
            dodged += 1
            enemy_speed += 1
            enemy_x = random.randrange(0, DISPLAY_WIDTH)

        if y < enemy_y + enemy_height:
            # print('Crossed Over')
            if(x > enemy_x and x < enemy_width + enemy_x):
                crashed()
            if(x+car_width < enemy_x and x+car_width > enemy_x):
                crashed()


            
                
            
        

        pygame.display.update()
        clock.tick(60)


intro()
game_loop()
pygame.quit()
