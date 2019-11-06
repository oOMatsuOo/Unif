import csv
import pygame
import math
import sys

#Constant

BLACK   = (  0,  0,  0)
RED     = (139,  0,  0)
PURPLE  = (148,  0,211)
GREY    = (105,105,105)
ORANGE  = (255,140,  0)
BLUE    = ( 30,144,237)
BROWN   = (188,143,143)

#Parameter

game = True

screen_size = (1000,1000)
width = 21
height= 0

case_size = screen_size[0]//10

framerate = 120

field = {}

camera_position = [1100, 0]

deplacement = case_size // 4


#Function

def stay_at_screen():
    global camera_position

    if camera_position[0] < 0:
        camera_position[0] = 0
    
    if camera_position[1] > 0:
        camera_position[1] = 0
    
    if camera_position[0] > (((width) * case_size) - screen_size[0]):
        camera_position[0] = (((width) * case_size) - screen_size[0])

    if camera_position[1] < (-((height) * case_size) + screen_size[1]):
        camera_position[1] = (-((height) * case_size) + screen_size[1])

def manage_keys(key):
    global camera_position

    if key == pygame.K_LEFT:
        camera_position[0] -= deplacement
    elif key == pygame.K_RIGHT:
        camera_position[0] += deplacement
    elif key == pygame.K_UP:
        camera_position[1] += deplacement
    elif key == pygame.K_DOWN:
        camera_position[1] -= deplacement

    return

def coordinates_to_pixel(coord):
    
    coord_px = coord * case_size
    
    return(coord_px)

def create_square(x, y):

    p1 = (x,y)
    p2 = (x+case_size,y)
    p3 = (x+case_size,y+case_size)
    p4 = (x,y+case_size)


    return(p1, p2, p3, p4)

def define_type_case(type_case):
    if type_case == 0:
        color = GREY
    elif type_case == 1:
        color = BROWN
    elif type_case == 2:
        color = BLUE

    return(color)

def create_case(case_type, x, y):
    x_coord = coordinates_to_pixel(x)
    y_coord = coordinates_to_pixel(y)
    
    square = create_square(x_coord,y_coord)

    color = define_type_case(int(case_type))

    pygame.draw.polygon(window, color, square)
    return

def create_screen(camera_position):
    height_screen = screen_size[1]//case_size
    width_screen = screen_size[0]//case_size

    camY = -camera_position[1]//case_size
    camX = camera_position[0]//case_size

    #print(str(camX) + "  " +  str(camY))

    i = camY
    i_prime = 0
    while i < height_screen + camY :
        j = camX
        j_prime = 0
        while j < width_screen + camX:
            create_case(field[i][j], j_prime, i_prime)
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

    return

def create_field(width):
    global field, height

    case = {}

    with open("maps.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            case_count = 0
            case = {}

            while case_count < width:
                print(case_count)
                case[case_count] = row[case_count]
                case_count += 1
            
            field[line_count] = case
            line_count += 1
        print(f"Processed {line_count} lines")
        print(f"Processed {case_count} cases")

        height = (line_count)

    return

#Game

pygame.init()

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

clock = pygame.time.Clock()
background_color = RED

pygame.key.set_repeat(10,10)

create_field(width)

while game:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            manage_keys(evenement.key)

    stay_at_screen()

    create_screen(camera_position)

    pygame.display.flip()

    clock.tick(framerate)