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

open_game = True
game = True

ratio = [9,16]

screen_size = [0,0]

width = 0
height= 0

framerate = 120

field = {}

camera_position = [0, 0]
spawn_point = []
collide = []

current_tile_1 = 0
current_tile_2 = 0

max_type_tile = 0


### Creation 

def create_field():
    global field, height, width, max_type_tile

    tile = {}
    with open("maps/map_1/maps.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        liste_field = list(csv_reader)
        width = len(liste_field[1])
        height = len(liste_field)


    with open("maps/map_1/maps.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            tile_count = 0
            tile = {}

            while tile_count < width:
                tile[tile_count] = row[tile_count]
                if int(tile[tile_count]) > max_type_tile:
                    max_type_tile = int(tile[tile_count])
                tile_count += 1
            
            field[line_count] = tile
            line_count += 1

        print(f"Processed {line_count} lines")
        print(f"Processed {tile_count} tiles")

    return

def create_collide():
    global collide

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        liste_properties = list(csv_reader)
        properties_width = len(liste_properties[1])

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            tile_count = 0

            while tile_count < properties_width:
                if row[tile_count] == "collide":
                    line_collide = tile_count
                    tile_count = properties_width
                tile_count += 1
            
            if not row[line_collide] in collide and row[line_collide] != "collide":
                collide.append(row[line_collide])

def create_spawn_point():
    global spawn_point

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        liste_properties = list(csv_reader)
        properties_width = len(liste_properties[1])

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            tile_count = 0

            while tile_count < properties_width:
                if row[tile_count] == "spawn_point":
                    line_spawn_point = tile_count
                    tile_count = properties_width
                tile_count += 1
            
            if row[line_spawn_point] != "spawn_point":
                spawn_point.append(int(row[line_spawn_point]))

    return

def create_tile(tile_type, x, y):
    x_coord = coordinates_to_pixel(x)
    y_coord = coordinates_to_pixel(y)
    
    square = create_square(x_coord,y_coord)

    color = define_type_tile(int(tile_type))

    pygame.draw.polygon(window, color, square)
    return

def create_square(x, y):

    p1 = (x,y)
    p2 = (x+tile_size,y)
    p3 = (x+tile_size,y+tile_size)
    p4 = (x,y+tile_size)


    return(p1, p2, p3, p4)


### Define

def define_screen_size(ratio):
    global screen_size, tile_size, movement,divide_tile

    different_screen_size = [426,640,768,800,848,896,960,1024,1152,1280,1366,1600,1920] 

    screen_size[0] = different_screen_size[6]
    screen_size[1] = int(screen_size[0] * ratio[0] / ratio[1])

    tile_size = 0
    start_tile_size = 60

    while tile_size == 0:
        if whole_divisor(screen_size[0],start_tile_size) and whole_divisor(screen_size[1],start_tile_size):
            tile_size = start_tile_size
        start_tile_size += 1

    divide_tile = 1

    movement = tile_size

    return

def define_spawn_point():
    global player_field_position,player_position,camera_position

    if spawn_point[1] <= screen_tile_size[1] // 2:
        camera_position[1] = 0
    else:
        camera_position[1] = - spawn_point[1] * tile_size + ( screen_tile_size[1] // 2 * tile_size)

    if spawn_point[0] <= screen_tile_size[0] // 2:
        camera_position[0] = 0
    else:
        camera_position[0] = spawn_point[0] * tile_size - screen_tile_size[0] // 2 * tile_size


    return


### Movement

def stay_at_screen():
    global camera_position

    if camera_position[0] <= 0:
        camera_position[0] = 0
    
    if camera_position[1] >= 0:
        camera_position[1] = 0
    
    if camera_position[0] > (width - 1) * tile_size - screen_size[0]:
        camera_position[0] = (width) * tile_size - screen_size[0]

    if camera_position[1] < - (height - 1) * tile_size + screen_size[1]:
        camera_position[1] = - (height) * tile_size + screen_size[1]
    
    
    return

def movement_up():
    
    camera_position[1] += movement  

    return

def movement_down():

    camera_position[1] -= movement

    return

def movement_left():

    camera_position[0] -= movement

    return

def movement_right():

    camera_position[0] += movement
    
    return


### Display

def display_game_screen():
    
    height_screen = screen_size[1] // tile_size
    width_screen = screen_size[0] // tile_size

    camera_tile_Y = -camera_position[1] // tile_size
    camera_tile_X = camera_position[0] // tile_size

    i = camera_tile_Y
    i_prime = (camera_position[1] / tile_size % 1)
    borne_i = height_screen + camera_tile_Y + 1
    if borne_i >= height:
        borne_i = height

    j_first = (camera_position[0]/tile_size % 1)
    borne_j = width_screen + camera_tile_X + 1
    if borne_j >= width:
        borne_j = width
    
    if i_prime % 1 != 0:
        i_prime = -1 + i_prime
        borne_i = height_screen + camera_tile_Y + 1


    if j_first % 1 != 0:
        j_first = - j_first
        borne_j = width_screen + camera_tile_X + 1


    while i < borne_i :
        j = camera_tile_X
        j_prime = j_first
        while j <  borne_j:
            create_tile(field[i][j], j_prime, i_prime)
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

    return


### Action

def manage_game_keys(type_key,evement):
    global camera_position, current_tile_2, current_tile_1

    if type_key == 2:
        if evenement.key == pygame.K_LEFT or evenement.key == pygame.K_q: 
            movement_left()

        elif evenement.key == pygame.K_RIGHT or evenement.key == pygame.K_d:
            movement_right()

        elif evenement.key == pygame.K_UP or evenement.key == pygame.K_z:
            movement_up()

        elif evenement.key == pygame.K_DOWN or evenement.key == pygame.K_s:
            movement_down()

        elif evement.key == pygame.K_KP_ENTER:
            for evenement2 in pygame.event.get():
                if evenement2.key == pygame.K_1:
                    for evement3 in pygame.event.get():
                        if evenement3.type == pygame.KEYDOWN:
                            if evement2.key == pygame.K_1:
                                provisor_key *= 10
                                provisor_key += 1
                            elif evenement3.type == pygame.K_2:
                                provisor_key *= 10
                                provisor_key += 2
                            elif evenement3.type == pygame.K_3:
                                provisor_key *= 10
                                provisor_key += 3
                            elif evenement3.type == pygame.K_4:
                                provisor_key *= 10
                                provisor_key += 4
                            elif evenement3.type == pygame.K_5:
                                provisor_key *= 10
                                provisor_key += 5
                            elif evenement3.type == pygame.K_6:
                                provisor_key *= 10
                                provisor_key += 6
                            elif evenement3.type == pygame.K_7:
                                provisor_key *= 10
                                provisor_key += 7
                            elif evenement3.type == pygame.K_8:
                                provisor_key *= 10
                                provisor_key += 8
                            elif evenement3.type == pygame.K_9:
                                provisor_key *= 10
                                provisor_key += 9
                        current_tile_1 = provisor_key
                        provisor_key = 0
                        
                if evenement2.key == pygame.K_2:
                    for evement3 in pygame.event.get():
                        if evenement3.type == pygame.KEYDOWN:
                            if evement2.key == pygame.K_1:
                                provisor_key *= 10
                                provisor_key += 1
                            elif evenement3.type == pygame.K_2:
                                provisor_key *= 10
                                provisor_key += 2
                            elif evenement3.type == pygame.K_3:
                                provisor_key *= 10
                                provisor_key += 3
                            elif evenement3.type == pygame.K_4:
                                provisor_key *= 10
                                provisor_key += 4
                            elif evenement3.type == pygame.K_5:
                                provisor_key *= 10
                                provisor_key += 5
                            elif evenement3.type == pygame.K_6:
                                provisor_key *= 10
                                provisor_key += 6
                            elif evenement3.type == pygame.K_7:
                                provisor_key *= 10
                                provisor_key += 7
                            elif evenement3.type == pygame.K_8:
                                provisor_key *= 10
                                provisor_key += 8
                            elif evenement3.type == pygame.K_9:
                                provisor_key *= 10
                                provisor_key += 9
                        current_tile_2 = provisor_key
                        provisor_key = 0


    elif type_key == 1:
        return

    return


### Calcul

def whole_divisor(x,n):
    
    return x %  n == 0

def define_type_tile(type_tile):
    if type_tile == 0:
        color = BLUE
    elif type_tile == 1:
        color = SAND
    elif type_tile == 2:
        color = GREEN
    elif type_tile == 3:
        color = GREY

    return(color)

def coordinates_to_pixel(coord):
    
    coord_px = coord * tile_size
    
    return(coord_px)

def pixel_to_coordinates(coord_px):

    coord = coord_px / tile_size

    return(coord)

def impress():
    print("CAM            : " + str(camera_position))
    print("Screen size    : " + str(screen_size))
    print("Tile size      : " + str(tile_size))
    print("Screen tile    : " + str(screen_tile_size))
    print("Collide        : " + str(collide))
    print("Move           : " + str(movement))
    print("Max tile       : " + str(max_type_tile))
    print("Current tile 1 : " + str(current_tile_1))
    print("Current tile 2 : " + str(current_tile_2))
    print("")

    return



### Game

pygame.init()

define_screen_size(ratio)
screen_tile_size = (pixel_to_coordinates(screen_size[0]), pixel_to_coordinates(screen_size[1]))
create_spawn_point()
define_spawn_point()

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Map Creator")

clock = pygame.time.Clock()
background_color = GREY

pygame.key.set_repeat(100,50)

create_field()
create_collide()

while open_game:
    now = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif game:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_game_keys(1,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_game_keys(2,evenement)
    
    if game:
        ### Game

        window.fill(background_color)

        stay_at_screen()

        display_game_screen()

        impress()

        pygame.display.flip()
    
    clock.tick(framerate)