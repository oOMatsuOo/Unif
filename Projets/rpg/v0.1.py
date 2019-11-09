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
SAND    = (230,184, 87)
GREEN   = (106,230, 87)

#Parameter

game = True

screen_size = (800,600)

width = 32
height= 0

case_size = screen_size[0]//20

framerate = 60

field = {}

camera_position = [0, 0]

movement = case_size

middle = 0


#Function

def stay_at_screen():
    global player_position

    if player_position[0] <= 0:
        player_position[0] = 0
    
    if player_position[1] >= 0:
        player_position[1] = 0
    
    if player_position[0] >= screen_size[0] - case_size:
        player_position[0] = screen_size[0] - case_size

    if player_position[1] <= -screen_size[1] + case_size:
        player_position[1] = -screen_size[1] + case_size
    
    return

def manage_keys(key):
    global player_position, camera_position

    if key == pygame.K_LEFT:

        if camera_position[0] == 0 and player_position[0] <= screen_size[0] // 2:
            camera_position[0] = 0
            player_position[0] -= movement

        elif camera_position[0] ==  (((width) * case_size) - screen_size[0]) and player_position[0] > screen_size[0] // 2:
            player_position[0] -= movement

        else:
            camera_position[0] -= movement

    elif key == pygame.K_RIGHT:

        if camera_position[0] == 0 and player_position[0] < screen_size[0] // 2:
            camera_position[0] = 0
            player_position[0] += movement

        elif camera_position[0] >= (((width) * case_size) - screen_size[0]) and player_position[0] >= screen_size[0] // 2:
            camera_position[0] = (((width) * case_size) - screen_size[0])
            player_position[0] += movement

        else:
            camera_position[0] += movement

    elif key == pygame.K_UP:

        if camera_position[1] == 0 and player_position[0] >= -screen_size[1] // 2:
            camera_position[1] = 0
            player_position[1] += movement

        elif camera_position[1] == (-((height) * case_size) + screen_size[1]) and player_position[1] <= -screen_size[1] // 2:
            player_position[1] += movement

        else:
            camera_position[1] += movement

    elif key == pygame.K_DOWN:

        if camera_position[1] == 0 and player_position[1] >= -screen_size[1] // 2:
            camera_position[1] = 0
            player_position[1] -= movement

        elif camera_position[1] == (-((height) * case_size) + screen_size[1]) and player_position[1] <= screen_size[1] // 2:
            camera_position[1] = (-((height) * case_size) + screen_size[1])
            player_position[1] -= movement

        else:
            camera_position[1] -= movement

    return

def coordinates_to_pixel(coord):
    
    coord_px = coord * case_size
    
    return(coord_px)

def pixel_to_coordinates(coord_px):

    coord = coord_px // case_size

    return(coord)

def create_square(x, y):

    p1 = (x,y)
    p2 = (x+case_size,y)
    p3 = (x+case_size,y+case_size)
    p4 = (x,y+case_size)


    return(p1, p2, p3, p4)

def define_type_case(type_case):
    if type_case == 0:
        color = BLUE
    elif type_case == 1:
        color = SAND
    elif type_case == 2:
        color = GREEN
    elif type_case == 3:
        color = GREY

    return(color)

def create_case(case_type, x, y):
    x_coord = coordinates_to_pixel(x)
    y_coord = coordinates_to_pixel(y)
    
    square = create_square(x_coord,y_coord)

    color = define_type_case(int(case_type))

    pygame.draw.polygon(window, color, square)
    return

def create_screen():
    height_screen = screen_size[1]//case_size
    width_screen = screen_size[0]//case_size

    camY = -camera_position[1]//case_size
    camX = camera_position[0]//case_size

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

    with open("maps/map_1/maps.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            case_count = 0
            case = {}

            while case_count < width:
                case[case_count] = row[case_count]
                case_count += 1
            
            field[line_count] = case
            line_count += 1
        print(f"Processed {line_count} lines")
        print(f"Processed {case_count} cases")

        height = (line_count)

    return

def create_player():
    square = create_square(player_position[0],-player_position[1])
    color = BLACK

    pygame.draw.polygon(window, color, square)

    return

def calcul_player_field_position():
    global player_field_position

    player_field_position[0] = player_position[0] + camera_position[0] 
    player_field_position[1] = player_position[1] + camera_position[1]

    return

def impress():
    print("CAM          : " + str(camera_position))
    print("PLAYER       : " + str(player_position))
    print("Case         : " + str(case_size))
    print("Player field : " + str(player_field_position))
    print("Height       : " + str(height * case_size))
    print("Width        : " + str(width * case_size))
    print("Screen case  : " + str(screen_case_size))
    print("")

def player_collide():
    global player_field_position; player_position

    collision = []

    return


#Game

pygame.init()

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

clock = pygame.time.Clock()
background_color = RED

pygame.key.set_repeat(50,50)

create_field(width)

screen_case_size = (pixel_to_coordinates(screen_size[0]), pixel_to_coordinates(screen_size[1]))
player_position = [pixel_to_coordinates((coordinates_to_pixel(screen_size[0])//2)),pixel_to_coordinates((coordinates_to_pixel(-screen_size[1])//2))]
player_field_position = [player_position[0], player_position[1]]

while game:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            manage_keys(evenement.key)

    stay_at_screen()

    calcul_player_field_position()

    impress()

    create_screen()

    create_player()

    pygame.display.flip()

    clock.tick(framerate)