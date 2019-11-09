import csv
import pygame
import math
import sys

### CONSTANT ###

BLACK   = (  0,  0,  0)
RED     = (139,  0,  0)
PURPLE  = (148,  0,211)
GREY    = (105,105,105)
ORANGE  = (255,140,  0)
BLUE    = ( 30,144,237)
BROWN   = (188,143,143)
SAND    = (230,184, 87)
GREEN   = (106,230, 87)

### PARAMETER ###

game = True

screen_size = (800,600)

width = 34
height= 0

case_size = screen_size[0]//20

framerate = 60

field = {}

camera_position = [0, 0]

movement = case_size//2

middle = 0

properties_width = 1

collide = []


### FUNCTION ###


### Creation ###


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

def create_collide(properties_width):
    global collide

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:

            case_count = 0

            while case_count < properties_width:
                if row[case_count] == "collide":
                    line_collide = case_count
                    case_count = properties_width
                case_count += 1
            
            if not row[line_collide] in collide and row[line_collide] != "collide":
                collide.append(row[line_collide])

def create_screen():
    height_screen = screen_size[1]//case_size
    width_screen = screen_size[0]//case_size

    camY = -camera_position[1] // case_size
    camX = camera_position[0] // case_size

    i = camY
    i_prime = (camera_position[1]/case_size % 1)
    borne_i = height_screen + camY

    j_first = (camera_position[0]/case_size % 1)
    borne_j = width_screen + camX 
    
    if i_prime % 1 != 0:
        i_prime = -1 + i_prime
        borne_i = height_screen + camY + 1


    if j_first % 1 != 0:
        j_first = - j_first
        borne_j = width_screen + camX + 1


    while i < borne_i :
        j = camX
        j_prime = j_first
        while j <  borne_j:
            create_case(field[i][j], j_prime, i_prime)
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

    return

def create_player():
    square = create_square(player_position[0],-player_position[1])
    color = BLACK

    pygame.draw.polygon(window, color, square)

    return

def create_case(case_type, x, y):
    x_coord = coordinates_to_pixel(x)
    y_coord = coordinates_to_pixel(y)
    
    square = create_square(x_coord,y_coord)

    color = define_type_case(int(case_type))

    pygame.draw.polygon(window, color, square)
    return

def create_square(x, y):

    p1 = (x,y)
    p2 = (x+case_size,y)
    p3 = (x+case_size,y+case_size)
    p4 = (x,y+case_size)


    return(p1, p2, p3, p4)


### Movement ###


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

def player_collide():
    global player_field_position, player_position

    player_case_position = [player_field_position[0] // case_size , player_field_position[1] // case_size]

    test_case_up = player_case_position[1] + 1  
    test_case_left = player_case_position[0]
    test_case_down = player_case_position[1] 
    test_case_right = player_case_position[0] + 1

    print("Test UP      : " + str(test_case_up))
    print("Test LEFT    : " + str(test_case_left))
    print("Test DOWN    : " + str(test_case_down))
    print("Test RIGHT   : " + str(test_case_right))

    if field[test_case_left][-test_case_up] in collide:
        player_field_position[1] = ( test_case_up + 1 ) * case_size


    return


### Action ###


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



### Calcul ###


def coordinates_to_pixel(coord):
    
    coord_px = coord * case_size
    
    return(coord_px)

def pixel_to_coordinates(coord_px):

    coord = coord_px // case_size

    return(coord)

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
    print("Collide      : " + str(collide))
    print("")

    return



### GAME ###

pygame.init()

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

clock = pygame.time.Clock()
background_color = RED

pygame.key.set_repeat(50,50)

create_field(width)
create_collide(properties_width)

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

    player_collide()

    impress()

    create_screen()

    create_player()

    pygame.display.flip()

    clock.tick(framerate)