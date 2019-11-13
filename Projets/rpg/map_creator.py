import csv
import pygame
import math

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

ratio = [9,16]

screen_size = [0,0]

width = 0
height= 0

framerate = 120

field = {}

camera_position = [0, 0]


### Creation 

def create_field():
    global field, height, width

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
                tile_count += 1
            
            field[line_count] = tile
            line_count += 1

        print(f"Processed {line_count} lines")
        print(f"Processed {tile_count} tiles")

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

    divide_tile = 2
    movement = tile_size / 8

    while tile_size % movement != 0:
        movement = tile_size // divide_tile
        divide_tile += 1

    return
