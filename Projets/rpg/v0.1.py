import csv
import pygame
import math
import sys

#Constant

BLACK   = (  0,  0,  0)
RED     = (139,  0,  0)
PURPLE  = (148,  0,211)
Grey    = (105,105,105)
ORANGE  = (255,140,  0)

#Parameter

game = True

case_size = 40

screen_size = (800,600)
width = 19

height_case = screen_size[1] / case_size
width_case = screen_size[0] / case_size

framerate = 60

field = {}

camera_position = (400, -300)


#Function

def manage_keys(key):
    return

def create_case(case_type, x, y):
    
    

    pygame.draw.polygon(window, color, square)
    return

def create_screen(camera):
    Xc, Yc = camera
    start_case_position = (Xc - screen_size[0] // 2, Yc + screen_size[1] // 2)

    X_start = start_case_position[0] // 40
    Y_start = start_case_position[1] // 40

    i = 0
    while i < height_case:
        j = 0
        while j < width_case:
            #print(field[X_start + i])
            print(j)
            j += 1
        print(i)
        i += 1
    

    return

def create_field(width):
    global field

    case = {}

    with open("maps.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            case_count = 0

            while case_count < width:
                case["id"] = case_count
                case["type"] = row[case_count]
                case_count += 1
            
            field[line_count] = case
            line_count += 1
        print(f"Processed {line_count} lines")
        print(f"Processed {case_count + 1} cases")


    return

#Game

pygame.init()

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

clock = pygame.time.Clock()
background_color = RED

pygame.key.set_repeat(10,10)

create_field(width)

create_screen(camera_position)

while game:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            manage_keys(evenement.key)

    window.fill(background_color)

    pygame.display.flip()

    clock.tick(framerate)