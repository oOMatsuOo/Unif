#!/usr/bin/env python3.6

import csv
import random as rdm
import pygame
import math
import subprocess
import sys

### CONSTANT ###

BLACK      = (  0,  0,  0)
RED        = (139,  0,  0)
PURPLE     = (148,  0,211)
GREY       = (105,105,105)
LIGHT_GREY = (180,184,181)
ORANGE     = (255,140,  0)
BLUE       = ( 30,144,237)
BROWN      = (188,143,143)
SAND       = (230,184, 87)
GREEN      = (106,230, 87)
DARK_GREEN = ( 60,134, 33)
WHITE      = (255,255,255)

### PARAMETER ###

open_game = True

menu = True

game = False

game_menu = False

option = False

screen_resolution_menu = False

control_menu = False

inventory = False

squad_menu = False

player_stat_display = False

ratio = [9,16]

screen_size = [0,0]

width = 0
height= 0

framerate = 120
animation_duration = 150
is_animated = False
animation = 0

field = {}
field_object = {}

player_position = [0, 0]
camera_position = [0, 0]
spawn_point = []
inventory_size = 5
stat_heigth = 12
stat_squad_height = 13
doing_attack = 0
wich_attack = 1
which_target = -1

middle = 0

collide = []

player = {}
squad_color = {}
squad_font_rect = {}
squad_display = {}

game_color = PURPLE
option_color = PURPLE
screen_resolution_color = PURPLE
control_color = PURPLE
save_game_color = PURPLE
exit_game_color = PURPLE
player_font_color = PURPLE
stat_player_color = BLACK
stat_member_color = BLACK
cross_color = BLACK
cross_squad_color = BLACK
cross_stat_player_color = BLACK
cross_stat_member_color = BLACK
attack_color = BLACK
object_color = BLACK
run_color = BLACK
magical_color = BLACK
physical_color = BLACK
monster_1_color = RED
monster_2_color = RED
monster_3_color = RED
player_color = GREEN
squad1_color = GREEN
squad2_color = GREEN


### FUNCTION ###


### Screen ###


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

def define_spawn_point():
    global player,player_position,camera_position

    if spawn_point[1] <= screen_tile_size[1] // 2:
        player_position[1] = - spawn_point[1] * tile_size
        camera_position[1] = 0
    else:
        player_position[1] = - screen_tile_size[1] // 2 * tile_size
        camera_position[1] = - spawn_point[1] * tile_size + ( screen_tile_size[1] // 2 * tile_size)

    if spawn_point[0] <= screen_tile_size[0] // 2:
        player_position[0] = spawn_point[0] * tile_size
        camera_position[0] = 0
    else:
        player_position[0] = screen_tile_size[0] // 2 * tile_size
        camera_position[0] = spawn_point[0] * tile_size - screen_tile_size[0] // 2 * tile_size


    return


### Creation ###


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

def create_player():
    global player,height_save, player_stat,squad

    player = {}
    player_stat = {}
    component = {}
    squad = {}
    squad_number = 0

    with open("player/save1.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        liste_field = list(csv_reader)
        height_save = len(liste_field)

    with open("player/save1.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            tile_count = 1
            component = {}

            if row[0] == 'position':
                while tile_count < 3:
                    component[tile_count - 1] = int(row[tile_count])
                    tile_count += 1
                player['position'] = component

            elif row[0] == 'area':
                player['area'] = int(row[1])

            elif row[0] == 'orientation':
                player['orientation'] = int(row[1])
            
            elif row[0] == 'inventory':
                while tile_count < inventory_size + 1:
                    component[tile_count - 1] = int(row[tile_count])
                    player['inventory'] = component
                    tile_count += 1
            
            elif row[0] == 'player':
                tile_count = 0
                while tile_count < stat_heigth:
                    if tile_count == 0:
                        player_stat['Level'] = int(row[1])
                    elif tile_count == 1:
                        player_stat['XP'] = int(row[2])
                    elif tile_count == 2:
                        player_stat['Element'] = row[3]
                    elif tile_count == 3:
                        player_stat['HP'] = int(row[4])
                    elif tile_count == 4:
                        player_stat['HP max'] = int(row[5])
                    elif tile_count == 5:
                        player_stat['Physical attack'] = int(row[6])
                    elif tile_count == 6:
                        player_stat['Physical resistance'] = int(row[7])
                    elif tile_count == 7:
                        player_stat['Magical attack'] = int(row[8])
                    elif tile_count == 8:
                        player_stat['Magical resistance'] = int(row[9]) 
                    elif tile_count == 9:
                        player_stat['Speed'] = int(row[10])
                    elif tile_count == 10:
                        player_stat['Critical %'] = int(row[11])
                    elif tile_count == 11:
                        player_stat['Name'] = row[12]
                    tile_count += 1

            elif row[0] == 'squad':
                tile_count = 0
                squad[squad_number] = {}
                while tile_count < stat_squad_height:
                    if tile_count == 0:
                        squad[squad_number]['Name'] = row[1]
                    elif tile_count == 1:
                        squad[squad_number]['Level'] = int(row[2])
                    elif tile_count == 2:
                        squad[squad_number]['XP'] = int(row[3])
                    elif tile_count == 3:
                        squad[squad_number]['Element'] = row[4]
                    elif tile_count == 4:
                        squad[squad_number]['HP'] = int(row[5])
                    elif tile_count == 5:
                        squad[squad_number]['HP max'] = int(row[6])
                    elif tile_count == 6:
                        squad[squad_number]['Physical attack'] = int(row[7])
                    elif tile_count == 7:
                        squad[squad_number]['Physical resistance'] = int(row[8])
                    elif tile_count == 8:
                        squad[squad_number]['Magical attack'] = int(row[9]) 
                    elif tile_count == 9:
                        squad[squad_number]['Magical resistance'] = int(row[10])
                    elif tile_count == 10:
                        squad[squad_number]['Speed'] = int(row[11])
                    elif tile_count == 11:
                        squad[squad_number]['Critical %'] = int(row[12])
                    elif tile_count == 12:
                        squad[squad_number]['Present'] = int(row[13])
                    tile_count += 1
                squad_number += 1

            line_count += 1
    
    print(player)
    return

def create_monster():
    global monster_tab

    monster_tab = {}

    with open("Monster/monster.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")
        tile_count =  0

        for row in csv_reader:
            monster_tab[tile_count] = {}

            monster_tab[tile_count]['Name'] = row[0]
            monster_tab[tile_count]['HP'] = int(row[1])
            monster_tab[tile_count]['HP max'] = int(row[2])
            monster_tab[tile_count]['Element'] = row[3]
            monster_tab[tile_count]['XP'] = int(row[4])
            monster_tab[tile_count]['Physical attack'] = int(row[5])
            monster_tab[tile_count]['Physical resistance'] = int(row[6])
            monster_tab[tile_count]['Magical attack'] = int(row[7])
            monster_tab[tile_count]['Magical resistance'] = int(row[8])
            monster_tab[tile_count]['Speed'] = int(row[9])
            monster_tab[tile_count]['Critical %'] = int(row[10])

            tile_count += 1

def create_area():
    global area

    area = []

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ",")

        for row in csv_reader:
            if row[0] == 'area':
                area_csv = {}
                area_csv['Number'] = row[1]
                area_csv['X1'] = row[2]
                area_csv['Y1'] = row[3]
                area_csv['X2'] = row[4]
                area_csv['Y2'] = row[5]
                area_csv['Type'] = row[6]
                if area_csv['Type'] == 'fight':
                    area_csv['Monster 1'] = row[7]
                    area_csv['Monster 2'] = row[8]
                    area_csv['Monster 3'] = row[9]
                    area_csv['Monster min level'] = row[10]
                    area_csv['Monster max level'] = row[11]

                area.append(area_csv)
    print(area)

def create_object():
    global field_object

    object_csv = {}

    with open("maps/map_1/object.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        liste_field = list(csv_reader)
        width_object = len(liste_field[1])

    with open("maps/map_1/object.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            tile_count = 0
            object_csv = {}
            while tile_count < width_object:
                object_csv[tile_count] = row[tile_count]
                tile_count += 1
            
            field_object[line_count] = object_csv
            line_count += 1

        print(f"Processed {line_count} lines")
        print(f"Processed {tile_count} tiles")
 
    return

def create_collide():
    global collide

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            if row[0] == 'collide':
                for i in range(1,len(row)):
                    if not row[i] in collide and row[i] != "collide":
                        collide.append(row[i])

def create_spawn_point():
    global spawn_point

    spawn_point = {}

    with open("maps/map_1/properties.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:

            for row in csv_reader:
                if row[0] == 'spawn_point':
                    spawn_point[0] = int(row[1])
                    spawn_point[1] = int(row[2])

def create_tile(tile_type, x, y):
    x_coord = coordinates_to_pixel(x)
    y_coord = coordinates_to_pixel(y)
    
    if tile_type == '4':
        pygame.draw.circle(window,DARK_GREEN,(int(x_coord + tile_size // 2),int(y_coord + tile_size//2)),tile_size//2)
    
    else :
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

def create_player_sprite():
    global sprite_player

    sprite_player = {}

    for name_image , name_file in ((1, 'front_stand.png'),
                                    (3, 'back_stand.png'),
                                    (2, 'right_stand.png'),
                                    (4, 'left_stand.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (tile_size,tile_size))
        add_position(sprite_player,name_image,image)

def create_player_animation_sprite():
    global sprite_left,sprite_right,sprite_front,sprite_back

    sprite_left = {
        'next_move_moment':None,
        'choreography':[]
    }
    sprite_right = {
        'next_move_moment':None,
        'choreography':[]
    }
    sprite_front = {
        'next_move_moment':None,
        'choreography':[]
    }
    sprite_back = {
        'next_move_moment':None,
        'choreography':[]
    }

    for name_image, name_file in (('left_left','left_left.png'),
                                ('left_right', 'left_right.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (tile_size,tile_size))
        sprite_left['choreography'].append((name_image,image))
    
    for name_image, name_file in (('right_right','right_right.png'),
                                ('right_left','right_left.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (tile_size,tile_size))
        sprite_right['choreography'].append((name_image,image))
    
    for name_image, name_file in (('front_right','front_right.png'),
                                ('front_left','front_left.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (tile_size,tile_size))
        sprite_front['choreography'].append((name_image,image))

    for name_image, name_file in (('back_right','back_right.png'),
                                ('back_left','back_left.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (tile_size,tile_size))
        sprite_back['choreography'].append((name_image,image))


### Movement ###


def stay_at_screen():
    global player_position

    if player_position[0] <= 0:
        player_position[0] = 0
    
    if player_position[1] >= 0:
        player_position[1] = 0
    
    if player_position[0] >= screen_size[0] - tile_size:
        player_position[0] = screen_size[0] - tile_size

    if player_position[1] <= -screen_size[1] + tile_size:
        player_position[1] = -screen_size[1] + tile_size
    
    return

def movement_up():

    if camera_position[1] == 0 and player_position[0] >= -screen_size[1] // 2:
        camera_position[1] = 0
        player_position[1] += movement

    elif camera_position[1] == (-((height) * tile_size) + screen_size[1]) and player_position[1] <= -screen_size[1] // 2:
        player_position[1] += movement

    else:
        camera_position[1] += movement
    
    if player_fight_area():
            if_fight()

    return

def movement_down():

    if camera_position[1] == 0 and player_position[1] >= -screen_size[1] // 2:
        camera_position[1] = 0
        player_position[1] -= movement

    elif camera_position[1] == (-((height) * tile_size) + screen_size[1]) and player_position[1] <= screen_size[1] // 2:
        camera_position[1] = (-((height) * tile_size) + screen_size[1])
        player_position[1] -= movement

    else:
        camera_position[1] -= movement

    if player_fight_area():
            if_fight()

    return

def movement_left():

    if camera_position[0] == 0 and player_position[0] <= screen_size[0] // 2:
        camera_position[0] = 0
        player_position[0] -= movement

    elif camera_position[0] ==  (((width) * tile_size) - screen_size[0]) and player_position[0] > screen_size[0] // 2:
        player_position[0] -= movement

    else:
        camera_position[0] -= movement
    
    if player_fight_area():
            if_fight()

    return

def movement_right():

    if camera_position[0] == 0 and player_position[0] < screen_size[0] // 2:
        camera_position[0] = 0
        player_position[0] += movement

    elif camera_position[0] >= (((width) * tile_size) - screen_size[0]) and player_position[0] >= screen_size[0] // 2:
        camera_position[0] = (((width) * tile_size) - screen_size[0])
        player_position[0] += movement

    else:
        camera_position[0] += movement

    if player_fight_area():
            if_fight()

    return


### Action ###


def manage_game_keys(key):
    global player_position, camera_position, player, menu, game, game_menu, inventory, squad_menu

    if key == pygame.K_LEFT or key == pygame.K_q:
        if player['position'][0] % tile_size == 0:
            if player['position'][1] % tile_size == 0:
                if not field[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide :
                    if not field_object[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide :
                        movement_left()
         
            else:
                if not field[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide and not field[-player['position'][1] // tile_size + 1][player['position'][0]//tile_size - 1] in collide:
                    if not field_object[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide and not field_object[-player['position'][1] // tile_size + 1][player['position'][0]//tile_size - 1] in collide:
                        movement_left()

        else:
            movement_left()
        
        player['orientation'] = 4
        start_animation_left(now)

    elif key == pygame.K_RIGHT or key == pygame.K_d:
        if player['position'][0] % tile_size == 0:
            if player['position'][1] % tile_size == 0:
                if not field[-player['position'][1] // tile_size][player['position'][0] // tile_size + 1] in collide :
                    if not field_object[-player['position'][1] // tile_size][player['position'][0] // tile_size + 1] in collide :
                        movement_right()
            else:
                if not field[-player['position'][1] // tile_size][player['position'][0] // tile_size + 1] in collide and not field[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size + 1] in collide:
                    if not field_object[-player['position'][1] // tile_size][player['position'][0] // tile_size + 1] in collide and not field_object[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size + 1] in collide:
                        movement_right()
        else:
            movement_right()
        
        player['orientation'] = 2
        start_animation_right(now)
        
    elif key == pygame.K_UP or key == pygame.K_z:
        if player['position'][1] % tile_size == 0:
            if player['position'][0] % tile_size == 0:
                if not field[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size] in collide :
                    if not field_object[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size] in collide :
                        movement_up()
                    
            else:
                if not field[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size] in collide and not field[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size + 1] in collide :
                    if not field_object[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size] in collide and not field_object[-player['position'][1] // tile_size - 1][player['position'][0] // tile_size + 1] in collide :
                        movement_up()

        else:
            movement_up()
        
        player['orientation'] = 3
        start_animation_back(now)

    elif key == pygame.K_DOWN or key == pygame.K_s:
        if player['position'][1] % tile_size == 0:
            if player['position'][0] % tile_size == 0:
                if not field[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size] in collide:
                    if not field_object[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size] in collide:
                        movement_down()
            else:
                if not field[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size] in collide and not field[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size + 1] in collide:
                    if not field_object[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size] in collide and not field_object[-player['position'][1] // tile_size + 1][player['position'][0] // tile_size + 1] in collide:
                        movement_down()
        else:
            movement_down()
        
        player['orientation'] = 1
        start_animation_front(now)
          
    elif key == pygame.K_ESCAPE:
        game_menu = True
        game = False

    elif key == pygame.K_i:
        game = False
        inventory = True
    
    elif key == pygame.K_u:
        game = False
        squad_menu = True

    return

def manage_menu_keys(type_key,evenement):
    global game_color, option_color, menu, option, game, open_game

    if type_key == -1:
        if rect_collide(game_rect ,pygame.mouse.get_pos()):
            game_color = RED
        elif rect_collide(option_rect ,pygame.mouse.get_pos()):
            option_color = RED
        else:
            option_color = PURPLE
            game_color = PURPLE

    elif type_key == 1:
        if evenement.button == 1:
                if rect_collide(game_rect ,pygame.mouse.get_pos()):
                    menu = False
                    game = True
                elif rect_collide(option_rect ,pygame.mouse.get_pos()):
                    menu = False
                    option = True
 
    elif type_key == 2 and evenement.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    return

def manage_inventory_keys(type_key, evenement):
    global cross_color,game,inventory

    if type_key == -1:
        if rect_collide(cross_rect,pygame.mouse.get_pos()):
            cross_color = RED
        else:
            cross_color = BLACK

    elif type_key == 2 and evenement.button == 1:
        if rect_collide(cross_rect, pygame.mouse.get_pos()):
            inventory = False
            game = True

    elif type_key == 1:
        if evenement.key == pygame.K_i:
            inventory = False
            game = True

def manage_squad_keys(type_key, evenement):
    global cross_squad_color,game,squad_menu, player_font_color,player_stat_display, squad_color

    if type_key == -1:
        for row in squad:
            if squad[row]['Present'] == 1:
                if rect_collide(squad_font_rect[row], pygame.mouse.get_pos()):
                    squad_color[row] = RED
                else:
                   squad_color[row] = PURPLE
                            
                    
        if rect_collide(cross_squad_rect,pygame.mouse.get_pos()):
            cross_squad_color = RED
        elif rect_collide(player_font_rect,pygame.mouse.get_pos()):
            player_font_color = RED
        else:
            cross_squad_color = BLACK
            player_font_color = PURPLE

    elif type_key == 2 and evenement.button == 1:
        if rect_collide(cross_squad_rect, pygame.mouse.get_pos()):
            squad_menu = False
            game = True
        elif rect_collide(player_font_rect, pygame.mouse.get_pos()):
            player_stat_display = True
            squad_menu = False

        for row in squad:
            if squad[row]['Present'] == 1:
                if rect_collide(squad_font_rect[row], pygame.mouse.get_pos()):
                    squad_display[row] = True
                    squad_menu = False
                            

    elif type_key == 1:
        if evenement.key == pygame.K_u:
            squad_menu = False
            game = True
    
    return

def manage_fight_keys(type_key, evenement):
    global doing_attack, attack_color, object_color, run_color, magical_color, physical_color

    if type_key == -1:
        if rect_collide(attack_rect,pygame.mouse.get_pos()):
            attack_color = RED
        elif rect_collide(use_object_rect, pygame.mouse.get_pos()):
            object_color = RED
        elif rect_collide(run_rect , pygame.mouse.get_pos()):
            run_color = RED
        elif rect_collide(magical_rect , pygame.mouse.get_pos()):
            magical_color = RED
        elif rect_collide(physical_rect , pygame.mouse.get_pos()):
            physical_color = RED
        else:
            attack_color = BLACK
            object_color = BLACK
            run_color = BLACK
            magical_color = BLACK
            physical_color = BLACK

    if type_key == 2 and evenement.button == 1:
        if rect_collide(attack_rect,pygame.mouse.get_pos()):
            doing_attack = 1
            return [0,0,0]
        elif rect_collide(use_object_rect, pygame.mouse.get_pos()):
            print("OBJET")
        elif rect_collide(run_rect , pygame.mouse.get_pos()):
            print("RUNNNN")
        if doing_attack:
            if rect_collide(magical_rect , pygame.mouse.get_pos()):
                return [1,wich_attack,'magical']
            elif rect_collide(physical_rect , pygame.mouse.get_pos()):
                return [1,wich_attack, 'physical']
    
    return [0,0,0]

def manage_choose_monster_keys(type_key, evenement, action, m1, m2, m3):
    global which_target, monster_1_color, monster_2_color, monster_3_color

    if type_key == -1:
        if rect_collide(sprite_m1, pygame.mouse.get_pos()) and m1 > 0:
            monster_1_color = BLUE
        elif rect_collide(sprite_m2, pygame.mouse.get_pos()) and m2 > 0:
            monster_2_color = BLUE
        elif rect_collide(sprite_m3, pygame.mouse.get_pos()) and m3 > 0:
            monster_3_color = BLUE
        else:
            monster_1_color = RED
            monster_2_color = RED
            monster_3_color = RED

    elif type_key == 2:
        if rect_collide(sprite_m1, pygame.mouse.get_pos()) and m1 > 0:
            which_target = 1
            return [2, 1, action[2]]
        elif rect_collide(sprite_m2, pygame.mouse.get_pos()) and m2 > 0:
            which_target = 2
            return [2, 2, action[2]]
        elif rect_collide(sprite_m3, pygame.mouse.get_pos()) and m3 > 0:
            which_target = 3
            return [2, 3, action[2]]

    return action
def manage_player_stat_keys(type_key, evenement):
    global cross_stat_player_color, player_stat_display, game

    if type_key == -1:
        if rect_collide(cross_stat_player_rect ,pygame.mouse.get_pos()):
            cross_stat_player_color = RED
        else:
            cross_stat_player_color = BLACK

    elif type_key == 1:
        return

    elif type_key == 2 and evenement.button == 1:
        if rect_collide(cross_stat_player_rect ,pygame.mouse.get_pos()):
            player_stat_display = False
            game = True

def manage_stat_member_keys(member,type_key, evenement):
    global cross_stat_member_color, game, squad_display

    if type_key == -1:
        if rect_collide(cross_stat_member_rect, pygame.mouse.get_pos()):
            cross_stat_member_color = RED
        else:
            cross_stat_member_color = BLACK
    elif type_key == 1:
        return
    elif type_key == 2 and evenement.button == 1:
        if rect_collide(cross_stat_member_rect, pygame.mouse.get_pos()):
            game = True
            squad_display[member] = False

    return

def manage_option_keys(type_key,evenement):
    global option, menu, screen_resolution_color, control_color,screen_resolution_menu,control_menu
    
    if evenement == -1:
        if rect_collide(screen_resolution_rect ,pygame.mouse.get_pos()):
            screen_resolution_color = RED
        elif rect_collide(control_rect ,pygame.mouse.get_pos()):
            control_color = RED
        else:
            screen_resolution_color = PURPLE
            control_color = PURPLE

    elif type_key == 1 and evenement.button == 1:
        if rect_collide(screen_resolution_rect ,pygame.mouse.get_pos()):
            option = False
            screen_resolution_menu = True
        elif rect_collide(control_rect ,pygame.mouse.get_pos()):
            option = False
            control_menu = True

    elif type_key == 2 and evenement.key == pygame.K_ESCAPE:
        option = False
        menu = True
    
    return

def manage_game_menu_keys(type_key,evenement):
    global save_game_color, exit_game_color,game_menu,game,menu

    if type_key == -1:
        if rect_collide(save_rect ,pygame.mouse.get_pos()):
            save_game_color = RED
        elif rect_collide(exit_game_rect ,pygame.mouse.get_pos()):
            exit_game_color = RED
        else:
            save_game_color = PURPLE
            exit_game_color = PURPLE

    elif type_key == 1:
        if rect_collide(save_rect ,pygame.mouse.get_pos()):
            save_game()
            game_menu = False
            game = True
        elif rect_collide(exit_game_rect ,pygame.mouse.get_pos()):
            save_game()
            game_menu = False
            game = False
            menu = True

    elif type_key == 2:
        if evenement.key == pygame.K_ESCAPE:
            game_menu = False
            game = True
    
    return


### Save ###


def save_game():

    field_list = []
    range_list = []

    for j in range (0,height_save):
        if j == 0:
            range_list.append('position')
            range_list.append(int(player['position'][0]//tile_size))
            range_list.append(int(-player['position'][1]//tile_size - 1))
        elif j == 1:
            range_list.append('area')
            range_list.append(int(player['area']))
        elif j == 2:
            range_list.append('orientation')
            range_list.append(player['orientation'])
        elif j == 3:
            range_list.append('inventory')

            for i in range (0,inventory_size):
                range_list.append(player['inventory'][i])
        elif j == 4:
            range_list.append('player')

            for i in range(0,stat_heigth):
                if i == 0:
                    range_list.append(player_stat['Level'])
                elif i == 1:
                    range_list.append(player_stat['XP'])
                elif i == 2:
                    range_list.append(player_stat['Element'])
                elif i == 3:
                    range_list.append(player_stat['HP'])
                elif i == 4:
                    range_list.append(player_stat['HP max'])
                elif i == 5:
                    range_list.append(player_stat['Physical attack'])
                elif i == 6:
                    range_list.append(player_stat['Physical resistance'])
                elif i == 7:
                    range_list.append(player_stat['Magical attack'])
                elif i == 8:
                    range_list.append(player_stat['Magical resistance']) 
                elif i == 9:
                    range_list.append(player_stat['Speed'])
                elif i == 10:
                    range_list.append(player_stat['Critical %'])
        
        for row in squad:
            if row + 5 == j:
                range_list.append('squad')

                for i in range(0, stat_squad_height):
                    if i == 0:
                        range_list.append(squad[row]['Name'])
                    elif i == 1:
                        range_list.append(squad[row]['Level'])
                    elif i == 2:
                        range_list.append(squad[row]['XP'])
                    elif i == 3:
                        range_list.append(squad[row]['Element'])
                    elif i == 4:
                        range_list.append(squad[row]['HP'])
                    elif i == 5:
                        range_list.append(squad[row]['HP max'])
                    elif i == 6:
                        range_list.append(squad[row]['Physical attack'])
                    elif i == 7:
                        range_list.append(squad[row]['Physical resistance'])
                    elif i == 8:
                        range_list.append(squad[row]['Magical attack']) 
                    elif i == 9:
                        range_list.append(squad[row]['Magical resistance'])
                    elif i == 10:
                        range_list.append(squad[row]['Speed'])
                    elif i == 11:
                        range_list.append(squad[row]['Critical %'])
                    elif i == 12:
                        range_list.append(squad[row]['Present'])

        field_list.append(range_list)
        range_list = []

    out = open("player/save1.csv",'w')
    outw = csv.writer(out)
    outw.writerows(field_list)
    out.close()
    return


### Fight ###


def player_fight_area():
    for i in area:
        if i['Type'] == 'fight' and int(i['Number']) == player['area']:
            return True

    return False

def if_fight():
    number = rdm.randint(0,100)

    if number <= 1:
        start_fight()

def which_monster():
    current_area = area[player['area']]  # Monster depends on the area

    monsters = [-1,-1,-1]

    monsters[0] = int(current_area['Monster 1'])
    monsters[1] = -1
    monsters[2] = -1

    if monsters[0] != current_area['Monster 2']:
        monsters[1] = int(current_area['Monster 2'])

    if monsters[0] != int(current_area['Monster 3']) and monsters[1] != int(current_area['Monster 3']):
        monsters[2] = int(current_area['Monster 3'])

    return (monsters)

def start_fight():
    global game

    game = False

    monsters = []
    monsters = which_monster() # Depends on the area of the player

    fight_monsters = [-1,-1,-1]
    fight_monsters[0] = monsters[0]

    if monsters[1] != -1:
        fight_monsters[1] = monsters[1]
        if monsters[2] != -1:
            fight_monsters[2] = monsters[2]

    fighting(create_fighting_monsters(fight_monsters))
    
    return
        
def create_fighting_monsters(fight_monsters):
    
    stat_monsters = {}
    i = 0

    for i in range(0,3):
        if(fight_monsters[i] != -1):
            stat_monsters[i] = monster_tab[fight_monsters[i]]

    return stat_monsters

def fighting(monsters):
    global game, action, attack, doing_attack

    monster_1 = {}
    monster_2 = {}
    monster_3 = {}

    number_monsters = 2
    monsters_added = -1
    actual_turn = 0
    current_fighter = {}

    for i in range(0,3):
        current_monster = {}
        while monsters_added != i:
            number = rdm.randint(0,number_monsters)

            try:
                monsters[number]['Name'] != " "
                current_monster = monsters[number]
                monsters_added += 1

                if i == 0:
                    monster_1 = create_monster_XP(current_monster)
                if i == 1:
                    monster_2 = create_monster_XP(current_monster)
                if i == 2:
                    monster_3 = create_monster_XP(current_monster)

            except:
                number_monsters -= 1

    while player_stat['HP'] > 0 and (monster_1['HP'] > 0 and monster_2['HP'] > 0 and monster_3['HP'] > 0):
        attack = 0

        fighters = [monster_1,monster_2,monster_3,player_stat,squad[0],squad[1]]
        
        number_fighter  = number_fighter_function()
        turn            = turn_fighter(monster_1["Speed"],monster_2["Speed"],monster_3["Speed"], number_fighter)

        current_fighter = fighters[turn[actual_turn]]
        print(current_fighter)
        
        action = [0,0,0]
        doing_attack = 0

        while (action[0] == 0) :

            display_fight_screen(current_fighter,fighters, number_fighter)

            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    action = manage_fight_keys(2, evenement)

            manage_fight_keys(-1, 0)

            pygame.display.flip()
        
        while action[0] == 1:
            
            for evenement in pygame.event.get():
                if evenement.type == pygame.MOUSEBUTTONDOWN:
                    action = manage_choose_monster_keys(2, evenement, action, monster_1['HP'], monster_2['HP'], monster_3['HP'])

            manage_choose_monster_keys(-1, 0, 0, monster_1['HP'], monster_2['HP'], monster_3['HP'])

            display_fight_screen(current_fighter,fighters, number_fighter)
            
            pygame.display.flip()
        
        while action[0] == 2:

            display_fight_animation_screen(current_fighter,fighters[action[1]], fighters, number_fighter)

            fighters[action[1]] = fight_calculator(current_fighter,fighters[action[1]], action[2])

            pygame.display.flip()

            action[0] = 0
        
        
        if actual_turn == number_fighter - 1:
            actual_turn = 0
        else:
            actual_turn += 1

        print(number_fighter)
        print(turn)

        monster_1['HP'] -= 10
        monster_2['HP'] -= 10
        monster_3['HP'] -= 10

    print('fin du combat')

    display_fight_screen(current_fighter,fighters, number_fighter)
    
    pygame.display.flip()


    pygame.time.wait(5000)

    game = True

    return

def create_monster_XP(monster):

    end_monster = {}
    current_area = area[player['area']]
    level = rdm.randint(int(current_area['Monster min level']), int(current_area['Monster max level']))

    end_monster['Name']                 = monster['Name']
    end_monster['HP']                   = int(monster['HP']) + level * 5
    end_monster['HP max']               = int(monster['HP max']) + level * 5
    end_monster['Element']              = monster['Element']
    end_monster['XP']                   = int(monster['XP']) + level * 10
    end_monster['Physical attack']      = int(monster['Physical attack']) + level
    end_monster['Physical resistance']  = int(monster['Physical resistance']) + level
    end_monster['Magical attack']       = int(monster['Magical attack']) + level
    end_monster['Magical resistance']   = int(monster['Magical resistance']) + level
    end_monster['Speed']                = int(monster['Speed']) + level // 2
    end_monster['Critical %']           = int(monster['Critical %']) + level // 2

    return end_monster

def fight_calculator(attacker, defender, attack_type):

    return defender

def number_fighter_function():
    number = 4

    if squad[0]['Present']:
        number += 1
        if squad[1]['Present']:
            number += 1

    return number

def turn_fighter(speed_m1,speed_m2,speed_m3,number_fighter):
    fighters = [-1,-1,-1,-1,-1,-1]
    
    speed = {}
    speed[0] = [0,speed_m1]
    speed[1] = [1,speed_m2]
    speed[2] = [2,speed_m3]
    speed[3] = [3,player_stat['Speed']]
    speed[4] = [4,squad[0]['Speed']]
    speed[5] = [5,squad[1]['Speed']]

    maximum = 0
    max_count = 0
    fighter_maximum = 0

    fighter_counter = 0

    while fighter_counter < number_fighter:
        max_count = 0
        maximum = 0
        fighter_maximum = 0

        while max_count < number_fighter:

            if speed[max_count][1] > maximum:
                fighter_maximum = speed[max_count][0]
                maximum = speed[max_count][1]

            max_count += 1

        speed[fighter_maximum][1] = 0

        fighters[fighter_counter] = fighter_maximum
        fighter_counter += 1

    return fighters



### Visual ###


def add_position(entity,name,image):
    entity[name] = image

    return

def display_player(time):

    if is_animated:
        if animation == 4:
            if sprite_left['next_move_moment'] - animation_duration > time:
                sprite = sprite_left['choreography'][0][1]
            else:
                sprite = sprite_left['choreography'][1][1]
        elif animation == 2:
            if sprite_right['next_move_moment'] - animation_duration > time:
                sprite = sprite_right['choreography'][0][1]
            else:
                sprite = sprite_right['choreography'][1][1]
        elif animation == 1:
            if sprite_front['next_move_moment'] - animation_duration > time:
                sprite = sprite_front['choreography'][0][1]
            else:
                sprite = sprite_front['choreography'][1][1]
        elif animation == 3:
            if sprite_back['next_move_moment'] - animation_duration > time:
                sprite = sprite_back['choreography'][0][1]
            else:
                sprite = sprite_back['choreography'][1][1]
    else :
        sprite = sprite_player[player['orientation']]

    window.blit(sprite,(player_position[0],-player_position[1]))

    return

def display_game_screen():
    
    height_screen = screen_size[1] // tile_size
    width_screen = screen_size[0] // tile_size

    camera_tile_Y = -camera_position[1] // tile_size
    camera_tile_X = camera_position[0] // tile_size

    i = camera_tile_Y
    i_prime = (camera_position[1] / tile_size % 1)
    borne_i = height_screen + camera_tile_Y + 1
    if borne_i >= height - 1:
        borne_i = height - 1

    j_first = (camera_position[0]/tile_size % 1)
    borne_j = width_screen + camera_tile_X + 1
    if borne_j >= width:
        borne_j = width - 1
    
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
            if field_object[i][j] != '1':
                create_tile(field_object[i][j], j_prime, i_prime)
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

    return

def display_game_menu_screen():
    global save_rect, exit_game_rect

    game_menu_first_rect = pygame.Rect(screen_size[0] // 200 * 3,screen_size[1] // 300 * 3 ,screen_size[0]//20 * 3 + screen_size[0] // 200 * 3 ,screen_size[1]//10 * 7 + 3 * screen_size[1] // 300 * 3)
    pygame.draw.rect(window,GREY,game_menu_first_rect)

    game_menu_rect = pygame.Rect(screen_size[0] // 100 * 2,screen_size[1] // 100 * 2 ,screen_size[0]//20 * 3 ,screen_size[1]//10 * 7)
    pygame.draw.rect(window,LIGHT_GREY,game_menu_rect)

    game_menu_font = pygame.font.SysFont("monospace", 40, True)

    save = game_menu_font.render("Save", True, save_game_color)
    save_size = game_menu_font.size("Save")
    exit_game = game_menu_font.render("Exit",True,exit_game_color)
    exit_game_size = game_menu_font.size("Exit")

    window.blit(save,(screen_size[0] // 100 * 4, screen_size[1] // 100 * 7))
    save_rect = pygame.Rect(screen_size[0] // 100 * 4, screen_size[1] // 100 * 7,save_size[0],save_size[1])
    window.blit(exit_game,(screen_size[0] // 100 * 4, screen_size[1] // 100 * 15))
    exit_game_rect = pygame.Rect(screen_size[0] // 100 * 4, screen_size[1] // 100 * 15,exit_game_size[0],exit_game_size[1])

    return

def display_inventory():
    global cross_rect

    inventory_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10 ,screen_size[0]// 10 * 8  ,screen_size[1]// 10 * 8)
    pygame.draw.rect(window,GREY,inventory_first_rect)

    inventory_rect = pygame.Rect(screen_size[0] // 10 + screen_size[0] // 200 * 3,screen_size[1] // 10 + screen_size[0] // 200 * 3 , screen_size[0]//10 * 8 - 2 * screen_size[0] // 200 * 3 ,screen_size[1]//10 * 8 - 2 *screen_size[0] // 200 * 3)
    pygame.draw.rect(window,LIGHT_GREY,inventory_rect)

    inventory_font = pygame.font.SysFont("monospace", 50, True)

    cross = inventory_font.render("X", True, cross_color)
    cross_size = inventory_font.size("X")

    cross_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10, cross_size[0] + 7, cross_size[1] + 7)
    pygame.draw.rect(window,GREY,cross_first_rect)

    window.blit(cross,(screen_size[0] // 10 + 5 , screen_size[1] // 10 + 5))
    cross_rect = pygame.Rect(screen_size[0] // 10 + 5, screen_size[1] // 10 + 5,cross_size[0],cross_size[1])

    return
    
def display_squad():
    global cross_squad_rect,player_font_rect,squad_font_rect,squad_color, squad_display

    squad_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10 ,screen_size[0]// 10 * 8  ,screen_size[1]// 10 * 8)
    pygame.draw.rect(window,GREY,squad_first_rect)

    squad_rect = pygame.Rect(screen_size[0] // 10 + screen_size[0] // 200 * 3,screen_size[1] // 10 + screen_size[0] // 200 * 3 , screen_size[0]//10 * 8 - 2 * screen_size[0] // 200 * 3 ,screen_size[1]//10 * 8 - 2 *screen_size[0] // 200 * 3)
    pygame.draw.rect(window,LIGHT_GREY,squad_rect)

    squad_font = pygame.font.SysFont("monospace", 50, True)

    cross = squad_font.render("X", True, cross_squad_color)
    cross_size = squad_font.size("X")

    player_font = squad_font.render("Player", True, player_font_color)
    player_font_size = squad_font.size("Player")

    for row in squad:
        if squad[row]['Present'] == 1:
            try:
                squad_color[row] = squad_color[row]
            except:
                squad_color[row] = PURPLE

            try:
                squad_display[row] = squad_display[row]
            except:
                squad_display[row] = False

            squad_row_font = squad_font.render(squad[row]['Name'], True, squad_color[row])
            squad_row_font_size = squad_font.size(squad[row]['Name'])
            
            window.blit(squad_row_font,(screen_size[0] // 10 * 2, screen_size[1] // 10 * (3 + row)))

            squad_font_rect[row] = pygame.Rect(screen_size[0] // 10 * 2,screen_size[1] // 10 * ( 3 + row), squad_row_font_size[0], squad_row_font_size[1])

    cross_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10, cross_size[0] + 7, cross_size[1] + 7)
    pygame.draw.rect(window,GREY,cross_first_rect)

    window.blit(cross,(screen_size[0] // 10 + 5 , screen_size[1] // 10 + 5))
    window.blit(player_font,(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2))

    cross_squad_rect = pygame.Rect(screen_size[0] // 10 + 5, screen_size[1] // 10 + 5,cross_size[0],cross_size[1])
    player_font_rect = pygame.Rect(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2,player_font_size[0],player_font_size[1])
    
    return

def display_stat_player():
    global cross_stat_player_rect

    stat_player_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10 ,screen_size[0]// 10 * 8  ,screen_size[1]// 10 * 8)
    pygame.draw.rect(window,GREY,stat_player_first_rect)

    stat_player_rect = pygame.Rect(screen_size[0] // 10 + screen_size[0] // 200 * 3,screen_size[1] // 10 + screen_size[0] // 200 * 3 , screen_size[0]//10 * 8 - 2 * screen_size[0] // 200 * 3 ,screen_size[1]//10 * 8 - 2 *screen_size[0] // 200 * 3)
    pygame.draw.rect(window,LIGHT_GREY,stat_player_rect)

    name_player_font = pygame.font.SysFont("monospace", 50, True)
    stat_player_font = pygame.font.SysFont("monospace", 35, True)
    player_font_size = stat_player_font.size("Player")

    XP_first_rect = pygame.Rect(screen_size[0]//10 * 6,screen_size[1]//10 * 2 + player_font_size[1] // 2, screen_size[0] // 10 * 2,screen_size[1] // 200 * 6)
    pygame.draw.rect(window,RED,XP_first_rect)

    cross_stat_player = name_player_font.render("X", True, cross_stat_player_color)
    cross_stat_player_size = name_player_font.size("X")

    player_font             = name_player_font.render("Player", True, stat_player_color)
    level_font              = stat_player_font.render("[ Lvl : " ,True, stat_player_color)
    stat_level_font         = stat_player_font.render(str(player_stat['Level']) + " ]", True, stat_player_color)
    element_font            = stat_player_font.render("[ Type : ", True, stat_player_color)
    stat_element_font       = stat_player_font.render(str(player_stat['Element']) + " ]", True, stat_player_color)
    HP_font                 = stat_player_font.render("[ HP : ", True, stat_player_color)
    stat_HP_font            = stat_player_font.render(str(player_stat['HP']) + " / " + str(player_stat['HP max']) + " ]", True, stat_player_color)
    ph_attack_font          = stat_player_font.render("Physical attack", True, stat_player_color)
    stat_attack_ph_font     = stat_player_font.render(str(player_stat['Physical attack']) , True, stat_player_color)
    ph_resistance_font      = stat_player_font.render("Physical resistance", True, stat_player_color)
    stat_resistance_ph_font = stat_player_font.render(str(player_stat['Physical resistance']), True, stat_player_color)
    mg_attack_font          = stat_player_font.render("Magical attack", True, stat_player_color)
    stat_attack_mg_font     = stat_player_font.render(str(player_stat['Magical attack']), True, stat_player_color)
    mg_resistance_font      = stat_player_font.render("Magical resistance", True, stat_player_color)
    stat_resistance_mg_font = stat_player_font.render(str(player_stat['Magical resistance']) , True, stat_player_color)
    speed_font              = stat_player_font.render("Speed", True, stat_player_color)
    stat_speed_font         = stat_player_font.render(str(player_stat['Speed']), True, stat_player_color)
    critical_font           = stat_player_font.render("Critical %", True, stat_player_color)
    stat_critical_font      = stat_player_font.render(str(player_stat['Critical %']), True, stat_player_color)

    cross_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10, cross_stat_player_size[0] + 7, cross_stat_player_size[1] + 7)
    pygame.draw.rect(window,GREY,cross_first_rect)

    window.blit(cross_stat_player,(screen_size[0] // 10 + 5 , screen_size[1] // 10 + 5))

    window.blit(player_font,(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2))

    window.blit(level_font,(screen_size[0] // 100 * 40  , screen_size[1] // 10 * 2))
    window.blit(stat_level_font,(screen_size[0] // 100 * 50, screen_size[1] // 10 * 2))

    window.blit(element_font,(screen_size[0]//100 * 25,screen_size[1] // 100 * 35))
    window.blit(stat_element_font, (screen_size[0] // 100 * 40,screen_size[1]// 100 * 35))

    window.blit(HP_font,(screen_size[0]//100 * 60,screen_size[1] // 100 * 35))
    window.blit(stat_HP_font, (screen_size[0] // 100 * 70, screen_size[1] // 100 * 35))

    window.blit(ph_attack_font,(screen_size[0] // 100 * 20, screen_size[1] // 100 * 50))
    window.blit(stat_attack_ph_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 50))

    window.blit(ph_resistance_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 50))
    window.blit(stat_resistance_ph_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 50))

    window.blit(mg_attack_font, (screen_size[0] // 100 * 20, screen_size[1] // 100 * 60))
    window.blit(stat_attack_mg_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 60))

    window.blit(mg_resistance_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 60))
    window.blit(stat_resistance_mg_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 60))

    window.blit(speed_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 70))
    window.blit(stat_speed_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 70))

    window.blit(critical_font, (screen_size[0] // 100 * 20, screen_size[1] // 100 * 70))
    window.blit(stat_critical_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 70))


    cross_stat_player_rect = pygame.Rect(screen_size[0] // 10 + 5, screen_size[1] // 10 + 5,cross_stat_player_size[0],cross_stat_player_size[1])
    
    return

def display_stat_member(number):
    global cross_stat_member_rect,cross_stat_member_color

    squad_member = squad[number]

    stat_member_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10 ,screen_size[0]// 10 * 8  ,screen_size[1]// 10 * 8)
    pygame.draw.rect(window,GREY,stat_member_first_rect)

    stat_member_rect = pygame.Rect(screen_size[0] // 10 + screen_size[0] // 200 * 3,screen_size[1] // 10 + screen_size[0] // 200 * 3 , screen_size[0]//10 * 8 - 2 * screen_size[0] // 200 * 3 ,screen_size[1]//10 * 8 - 2 *screen_size[0] // 200 * 3)
    pygame.draw.rect(window,LIGHT_GREY,stat_member_rect)

    name_member_font = pygame.font.SysFont("monospace", 50, True)
    stat_member_font = pygame.font.SysFont("monospace", 35, True)
    member_font_size = stat_member_font.size(squad_member['Name'])

    XP_first_rect = pygame.Rect(screen_size[0]//10 * 6,screen_size[1]//10 * 2 + member_font_size[1] // 2, screen_size[0] // 10 * 2,screen_size[1] // 200 * 6)
    pygame.draw.rect(window,RED,XP_first_rect)

    cross_stat_member = name_member_font.render("X", True, cross_stat_member_color)
    cross_stat_member_size = name_member_font.size("X")

    member_font             = name_member_font.render(squad_member['Name'], True, stat_member_color)
    level_font              = stat_member_font.render("[ Lvl : " ,True, stat_member_color)
    stat_level_font         = stat_member_font.render(str(squad_member['Level']) + " ]", True, stat_member_color)
    element_font            = stat_member_font.render("[ Type : ", True, stat_member_color)
    stat_element_font       = stat_member_font.render(str(squad_member['Element']) + " ]", True, stat_member_color)
    HP_font                 = stat_member_font.render("[ HP : ", True, stat_member_color)
    stat_HP_font            = stat_member_font.render(str(squad_member['HP']) + " / " + str(squad_member['HP max']) + " ]", True, stat_member_color)
    ph_attack_font          = stat_member_font.render("Physical attack", True, stat_member_color)
    stat_attack_ph_font     = stat_member_font.render(str(squad_member['Physical attack']) , True, stat_member_color)
    ph_resistance_font      = stat_member_font.render("Physical resistance", True, stat_member_color)
    stat_resistance_ph_font = stat_member_font.render(str(squad_member['Physical resistance']), True, stat_member_color)
    mg_attack_font          = stat_member_font.render("Magical attack", True, stat_member_color)
    stat_attack_mg_font     = stat_member_font.render(str(squad_member['Magical attack']), True, stat_member_color)
    mg_resistance_font      = stat_member_font.render("Magical resistance", True, stat_member_color)
    stat_resistance_mg_font = stat_member_font.render(str(squad_member['Magical resistance']) , True, stat_member_color)
    speed_font              = stat_member_font.render("Speed", True, stat_member_color)
    stat_speed_font         = stat_member_font.render(str(squad_member['Speed']), True, stat_member_color)
    critical_font           = stat_member_font.render("Critical %", True, stat_member_color)
    stat_critical_font      = stat_member_font.render(str(squad_member['Critical %']), True, stat_member_color)

    cross_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10, cross_stat_member_size[0] + 7, cross_stat_member_size[1] + 7)
    pygame.draw.rect(window,GREY,cross_first_rect)

    window.blit(cross_stat_member,(screen_size[0] // 10 + 5 , screen_size[1] // 10 + 5))

    window.blit(member_font,(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2))

    window.blit(level_font,(screen_size[0] // 100 * 40  , screen_size[1] // 10 * 2))
    window.blit(stat_level_font,(screen_size[0] // 100 * 50, screen_size[1] // 10 * 2))

    window.blit(element_font,(screen_size[0]//100 * 25,screen_size[1] // 100 * 35))
    window.blit(stat_element_font, (screen_size[0] // 100 * 40,screen_size[1]// 100 * 35))

    window.blit(HP_font,(screen_size[0]//100 * 60,screen_size[1] // 100 * 35))
    window.blit(stat_HP_font, (screen_size[0] // 100 * 70, screen_size[1] // 100 * 35))

    window.blit(ph_attack_font,(screen_size[0] // 100 * 20, screen_size[1] // 100 * 50))
    window.blit(stat_attack_ph_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 50))

    window.blit(ph_resistance_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 50))
    window.blit(stat_resistance_ph_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 50))

    window.blit(mg_attack_font, (screen_size[0] // 100 * 20, screen_size[1] // 100 * 60))
    window.blit(stat_attack_mg_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 60))

    window.blit(mg_resistance_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 60))
    window.blit(stat_resistance_mg_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 60))

    window.blit(speed_font, (screen_size[0] // 100 * 55, screen_size[1] // 100 * 70))
    window.blit(stat_speed_font, (screen_size[0] // 100 * 88, screen_size[1] // 100 * 70))

    window.blit(critical_font, (screen_size[0] // 100 * 20, screen_size[1] // 100 * 70))
    window.blit(stat_critical_font, (screen_size[0] // 100 * 48, screen_size[1] // 100 * 70))


    cross_stat_member_rect = pygame.Rect(screen_size[0] // 10 + 5, screen_size[1] // 10 + 5,cross_stat_member_size[0],cross_stat_member_size[1])
    
    return

def display_menu_screen():
    global game_rect, option_rect
    
    menu_font = pygame.font.SysFont("monospace", 100, True)
    list_font = pygame.font.SysFont("monospace", 50, True)

    menu = menu_font.render("MENU", True, ORANGE)
    menu_size = menu_font.size("MENU")
    game = list_font.render("Game", True, game_color)
    game_size = list_font.size("Game")
    option = list_font.render("Option",True,option_color)
    option_size = list_font.size("Option")

    window.blit(menu, (screen_size[0] // 2 - menu_size[0] // 2,screen_size[1]//10))
    window.blit(game,(screen_size[0] // 5, screen_size[1] // 9 * 3))
    game_rect = pygame.Rect(screen_size[0] // 5, screen_size[1] // 9 * 3,game_size[0],game_size[1])
    window.blit(option,(screen_size[0] // 5, screen_size[1] // 9 * 5))
    option_rect = pygame.Rect(screen_size[0] // 5, screen_size[1] // 9 * 5,option_size[0],option_size[1])

    return

def display_option_screen():
    global screen_resolution_rect, control_rect
    
    list_font = pygame.font.SysFont("monospace", 50, True)

    screen_resolution = list_font.render("Screen resolution", True, screen_resolution_color)
    screen_resolution_size = list_font.size("Screen resolution")
    control = list_font.render("Control",True, control_color)
    control_size = list_font.size("Control")

    window.blit(screen_resolution,(screen_size[0] // 5, screen_size[1] // 9 * 3))
    screen_resolution_rect = pygame.Rect(screen_size[0] // 5, screen_size[1] // 9 * 3, screen_resolution_size[0], screen_resolution_size[1])
    window.blit(control,(screen_size[0] // 5, screen_size[1] // 9 * 5))
    control_rect = pygame.Rect(screen_size[0] // 5, screen_size[1] // 9 * 5,control_size[0],control_size[1])

    
    return

def display_fight_screen(attacker,fighters, number_fighter):
    global attack_rect, use_object_rect, run_rect, magical_rect, physical_rect, attack, sprite_m1, sprite_m2, sprite_m3
    
    fight_font = pygame.font.SysFont("monospace", 50, True)
    name_font = pygame.font.SysFont("monospace", 35, True)

    background = BLACK

    sprite_m1 = pygame.Rect(screen_size[0] // 20 * 5 ,screen_size[1] // 20 , screen_size[0] // 20 * 2 ,screen_size[0] // 20 * 2)
    m1_name = name_font.render(fighters[0]['Name'], True, monster_1_color)
    sprite_m2 = pygame.Rect(screen_size[0] // 20 * 4 ,screen_size[1] // 20 * 5 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    m2_name = name_font.render(fighters[1]['Name'], True, monster_2_color)
    sprite_m3 = pygame.Rect(screen_size[0] // 20 * 3,screen_size[1] // 20 * 9 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    m3_name = name_font.render(fighters[2]['Name'], True, monster_3_color)

    sprite_player = pygame.Rect(screen_size[0] // 20 * 15 ,screen_size[1] // 20 * 3 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    player_name = name_font.render(fighters[3]['Name'], True, RED)
    sprite_squad1 = pygame.Rect(screen_size[0] // 20 * 14 ,screen_size[1] // 20 * 7  , screen_size[0] // 20 * 2 ,screen_size[0] // 20 * 2)
    squad1_name = name_font.render(fighters[4]['Name'], True, RED)
    sprite_squad2 = pygame.Rect(screen_size[0] // 20 * 13 ,screen_size[1] // 20 * 11 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    squad2_name = name_font.render(fighters[5]['Name'], True, RED)

    option_rect = pygame.Rect( 0 , screen_size[1] // 20 * 14, screen_size[0] // 20 * 11, screen_size[1] // 20 * 6 )
    option_bar  = pygame.Rect(screen_size[0] // 20 * 6, screen_size[1] // 20 * 14, screen_size[0] // 100, screen_size[1] // 20 * 6)

    attack = fight_font.render("Attack",True,attack_color)
    attack_size = fight_font.size("Attack")
    use_object = fight_font.render("Object", True, object_color)
    use_object_size = fight_font.size("Object")
    run = fight_font.render("Run", True, run_color)
    run_size = fight_font.size("Run")

    magical = fight_font.render("Magical", True, magical_color)
    magical_size = fight_font.size("Magical")
    physical = fight_font.render("Physical", True, physical_color)
    physical_size = fight_font.size("Physical")

    attack_rect = pygame.Rect(screen_size[0] // 20 * 7, screen_size[1] // 20 * 14 ,attack_size[0], attack_size[1])
    use_object_rect = pygame.Rect(screen_size[0] // 20 * 7, screen_size[1] // 20 * 16, use_object_size[0], use_object_size[1])
    run_rect = pygame.Rect(screen_size[0] // 20 * 7, screen_size[1] // 20 * 18, run_size[0], run_size[1])
    magical_rect = pygame.Rect(screen_size[0] // 20 * 1, screen_size[1] // 20 * 15, magical_size[0], magical_size[1])
    physical_rect = pygame.Rect(screen_size[0] // 20 * 1 , screen_size[1] // 20 * 17, physical_size[0], physical_size[1])


    window.fill(background)
    pygame.draw.rect(window,RED,sprite_m1)
    window.blit(m1_name, (screen_size[0] // 40 * 5 ,screen_size[1] // 40 * 3))
    pygame.draw.rect(window,RED,sprite_m2)
    window.blit(m2_name, (screen_size[0] // 40 * 3 ,screen_size[1] // 40 * 11))
    pygame.draw.rect(window,RED,sprite_m3)
    window.blit(m3_name, (screen_size[0] // 40 * 1,screen_size[1] // 40 * 19))

    pygame.draw.rect(window,GREEN,sprite_player)
    window.blit(player_name, (screen_size[0] // 40 * 35 ,screen_size[1] // 40 * 7))
    pygame.draw.rect(window,GREEN,sprite_squad1)
    window.blit(squad1_name, (screen_size[0] // 40 * 33 ,screen_size[1] // 40 * 16))
    pygame.draw.rect(window,GREEN,sprite_squad2)
    window.blit(squad2_name, (screen_size[0] // 40 * 31 ,screen_size[1] // 40 * 24))

    pygame.draw.rect(window,GREY,option_rect)
    pygame.draw.rect(window,BLACK,option_bar)

    window.blit(attack, (screen_size[0] // 20 * 7, screen_size[1] // 20 * 14))
    window.blit(use_object, (screen_size[0] // 20 * 7, screen_size[1] // 20 * 16))
    window.blit(run, (screen_size[0] // 20 * 7, screen_size[1] // 20 * 18))

    if doing_attack :
        window.blit(magical, (screen_size[0] // 20 * 1, screen_size[1] // 20 * 15))
        window.blit(physical, (screen_size[0] // 20 * 1 , screen_size[1] // 20 * 17))

    
    return

def display_fight_animation_screen(attacker, defender, fighters, number_fighter):
    global attack_rect, use_object_rect, run_rect, magical_rect, physical_rect, attack, sprite_m1, sprite_m2, sprite_m3

    m1_x_pos = screen_size[0] // 20 * 4
    m2_x_pos = screen_size[0] // 20 * 3
    m3_x_pos = screen_size[0] // 20 * 2

    player_x_pos = screen_size[0] // 20 * 16
    squad1_x_pos = screen_size[0] // 20 * 15
    squad2_x_pos = screen_size[0] // 20 * 14

    player_color = GREEN
    squad1_color = GREEN
    squad2_color = GREEN

    print(attacker, defender)

    fight_font = pygame.font.SysFont("monospace", 50, True)

    background = BLACK

    sprite_m1 = pygame.Rect(m1_x_pos ,screen_size[1] // 20 , screen_size[0] // 20 * 2 ,screen_size[0] // 20 * 2)
    sprite_m2 = pygame.Rect(m2_x_pos,screen_size[1] // 20 * 5 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    sprite_m3 = pygame.Rect(m3_x_pos,screen_size[1] // 20 * 9 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    
    sprite_player = pygame.Rect(player_x_pos ,screen_size[1] // 20 * 3 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)
    sprite_squad1 = pygame.Rect(squad1_x_pos ,screen_size[1] // 20 * 7  , screen_size[0] // 20 * 2 ,screen_size[0] // 20 * 2)
    sprite_squad2 = pygame.Rect(squad2_x_pos ,screen_size[1] // 20 * 11 , screen_size[0] // 20 * 2,screen_size[0] // 20 * 2)

    option_rect = pygame.Rect( 0 , screen_size[1] // 20 * 14, screen_size[0] // 20 * 13, screen_size[1] // 20 * 6 )
    option_bar  = pygame.Rect(screen_size[0] // 20 * 8, screen_size[1] // 20 * 14, screen_size[0] // 100, screen_size[1] // 20 * 6)

    attack = fight_font.render("Attack",True,attack_color)
    attack_size = fight_font.size("Attack")
    use_object = fight_font.render("Object", True, object_color)
    use_object_size = fight_font.size("Object")
    run = fight_font.render("Run", True, run_color)
    run_size = fight_font.size("Run")

    magical = fight_font.render("Magical", True, magical_color)
    magical_size = fight_font.size("Magical")
    physical = fight_font.render("Physical", True, physical_color)
    physical_size = fight_font.size("Physical")

    attack_rect = pygame.Rect(screen_size[0] // 20 * 9, screen_size[1] // 20 * 14 ,attack_size[0], attack_size[1])
    use_object_rect = pygame.Rect(screen_size[0] // 20 * 9, screen_size[1] // 20 * 16, use_object_size[0], use_object_size[1])
    run_rect = pygame.Rect(screen_size[0] // 20 * 9, screen_size[1] // 20 * 18, run_size[0], run_size[1])
    magical_rect = pygame.Rect(screen_size[0] // 20 * 2, screen_size[1] // 20 * 15, magical_size[0], magical_size[1])
    physical_rect = pygame.Rect(screen_size[0] // 20 * 2 , screen_size[1] // 20 * 17, physical_size[0], physical_size[1])


    window.fill(background)
    pygame.draw.rect(window,monster_1_color,sprite_m1)
    pygame.draw.rect(window,monster_2_color,sprite_m2)
    pygame.draw.rect(window,monster_3_color,sprite_m3)
    pygame.draw.rect(window,player_color,sprite_player)
    pygame.draw.rect(window,squad1_color,sprite_squad1)
    pygame.draw.rect(window,squad2_color,sprite_squad2)
    pygame.draw.rect(window,GREY,option_rect)
    pygame.draw.rect(window,BLACK,option_bar)

    window.blit(attack, (screen_size[0] // 20 * 9, screen_size[1] // 20 * 14))
    window.blit(use_object, (screen_size[0] // 20 * 9, screen_size[1] // 20 * 16))
    window.blit(run, (screen_size[0] // 20 * 9, screen_size[1] // 20 * 18))

    if doing_attack :
        window.blit(magical, (screen_size[0] // 20 * 2, screen_size[1] // 20 * 15))
        window.blit(physical, (screen_size[0] // 20 * 2 , screen_size[1] // 20 * 17))

    return

def rect_collide(rect,position):
    
    return rect.collidepoint(position)

def start_animation_left(time):
    global is_animated, animation, sprite_left
    
    if not is_animated or animation != 4:
        is_animated = True
        animation = 4
        sprite_left['next_move_moment'] = time + animation_duration * 2

    elif sprite_left['next_move_moment'] <= time:
        sprite_left['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_right(time):
    global is_animated, animation, sprite_right
    
    if not is_animated or animation != 2:
        is_animated = True
        animation = 2
        sprite_right['next_move_moment'] = time + animation_duration * 2

    elif sprite_right['next_move_moment'] <= time:
        sprite_right['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_front(time):
    global is_animated, animation, sprite_front
    
    if not is_animated or animation != 1:
        is_animated = True
        animation = 1
        sprite_front['next_move_moment'] = time + animation_duration * 2

    elif sprite_front['next_move_moment'] <= time:
        sprite_front['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_back(time):
    global is_animated, animation, sprite_back
    
    if not is_animated or animation != 3:
        is_animated = True
        animation = 3
        sprite_back['next_move_moment'] = time + animation_duration * 2

    elif sprite_back['next_move_moment'] <= time:
        sprite_back['next_move_moment'] = time + animation_duration * 2
        
        return


### Calcul ###!


def coordinates_to_pixel(coord):
    
    coord_px = coord * tile_size
    
    return(coord_px)

def pixel_to_coordinates(coord_px):

    coord = coord_px / tile_size

    return(coord)

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

def calcul_player_position():
    global player

    player['position'][0] = player_position[0] + camera_position[0] 
    player['position'][1] = player_position[1] + camera_position[1]

    return

def is_collide(position):
    
    if field[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide or field_object[-player['position'][1] // tile_size][player['position'][0] // tile_size - 1] in collide:
        return True
    else:
        return False

def impress():
    print("CAM          : " + str(camera_position))
    print("PLAYER       : " + str(player_position))
    print("Screen size  : " + str(screen_size))
    print("tile size    : " + str(tile_size))
    print("Player field : " + str(player['position']))
    print("Height       : " + str(height))
    print("Width        : " + str(width))
    print("Screen tile  : " + str(screen_tile_size))
    print("Collide      : " + str(collide))
    print("Orientation  : " + str(player['orientation']))
    print("Move         : " + str(movement))
    print("Animated     : " + str(is_animated))
    print("")

    return

def whole_divisor(x,n):
    
    return x %  n == 0
    
def is_always_animated(time):
    global is_animated

    if is_animated:
        if animation == 4:
            if sprite_left['next_move_moment'] < time:
                is_animated = False
        elif animation == 3:
            if sprite_back['next_move_moment'] < time:
                is_animated = False
        elif animation == 1:
            if sprite_front['next_move_moment'] < time:
                is_animated = False
        elif animation == 2:
            if sprite_right['next_move_moment'] < time:
                is_animated = False


### GAME ###


pygame.init()
background_color = GREY

define_screen_size(ratio)
screen_tile_size = (pixel_to_coordinates(screen_size[0]), pixel_to_coordinates(screen_size[1]))

window = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
pygame.display.set_caption("First RPG")

create_player()
create_monster()
create_spawn_point()
define_spawn_point()

clock = pygame.time.Clock()

pygame.key.set_repeat(50,25)

create_field()
create_object()
create_collide()
create_area()
create_player_sprite()
create_player_animation_sprite()

while open_game:
    now = pygame.time.get_ticks()
    is_always_animated(now)

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif game:
            if evenement.type == pygame.KEYDOWN:
                manage_game_keys(evenement.key)
        elif menu:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_menu_keys(1,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_menu_keys(2,evenement)
        elif option:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_option_keys(1,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_option_keys(2,evenement)
        elif game_menu:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_game_menu_keys(1,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_game_menu_keys(2,evenement)
        elif inventory:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_inventory_keys(2,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_inventory_keys(1,evenement)
        elif squad_menu:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_squad_keys(2,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_squad_keys(1,evenement)
        elif player_stat_display:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_player_stat_keys(2, evenement)

        for row in squad_display:
            if squad_display[row] and evenement.type == pygame.MOUSEBUTTONDOWN:    
                try :
                    manage_stat_member_keys(row,2,evenement)
                except:
                    display_stat_member(row)


    if menu:
        ### Menu

        window.fill(background_color)

        display_menu_screen()

        manage_menu_keys(-1,0)

        pygame.display.flip()
        

    elif game:
        ### Game
        
        stay_at_screen()

        calcul_player_position()

        #impress()

        display_game_screen()

        display_player(now)

        pygame.display.flip()


    elif inventory:
        ### Inventory

        display_inventory()

        manage_inventory_keys(-1,0)

        pygame.display.flip()


    elif squad_menu:
        ### Squad team
        display_squad()

        manage_squad_keys(-1,0)

        pygame.display.flip()


    elif player_stat_display:
        ### Player Stat Display
        
        display_stat_player()

        manage_player_stat_keys(-1,0)

        pygame.display.flip()


    elif game_menu:
        ### Game Menu

        display_game_menu_screen()
        
        manage_game_menu_keys(-1,0)
        
        pygame.display.flip()


    elif option:
        ### Option

        window.fill(background_color)
        
        display_option_screen()

        manage_option_keys(0,-1)

        pygame.display.flip()
    

    elif screen_resolution_menu:
        ### screen resolution option

        window.fill(background_color)

        #display_screen_resolution_screen()

        #manage_screen_resolution_keys(-1)
        screen_resolution_menu = False
        menu = True

        pygame.display.flip()


    elif control_menu:
        ### control option

        window.fill(background_color)

        #display_control_screen()

        #manage_control_keys(-1)
        control_menu = False
        menu = True

        pygame.display.flip()


    for row in squad_display:
        if squad_display[row]:
            ### Display member stat

            display_stat_member(row)

            manage_stat_member_keys(row,-1,0)

            pygame.display.flip()


    clock.tick(framerate)