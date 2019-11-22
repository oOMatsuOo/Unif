import csv
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

squad = False

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
stat_heigth = 9

middle = 0

collide = []

player = {}

game_color = PURPLE
option_color = PURPLE
screen_resolution_color = PURPLE
control_color = PURPLE
save_game_color = PURPLE
exit_game_color = PURPLE
player_font_color = PURPLE
cross_color = BLACK
cross_squad_color = BLACK


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
    global player,height_save, player_stat

    player = {}
    player_stat = {}
    component = {}
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
                player['position']= component

            elif row[0] == 'orientation':
                component[tile_count - 1] = int(row[tile_count])
                player['orientation'] = component
            
            elif row[0] == 'inventory':
                while tile_count < inventory_size + 1:
                    component[tile_count - 1] = int(row[tile_count])
                    player['inventory'] = component
                    tile_count += 1
            
            elif row[0] == 'player':
                tile_count = 1
                while tile_count < stat_heigth + 1:
                    if tile_count == 1:
                        player_stat['Level'] = int(row[1])
                    elif tile_count == 2:
                        player_stat['XP'] = int(row[2])
                    elif tile_count == 3:
                        player_stat['Element'] = row[3]
                    elif tile_count == 4:
                        player_stat['HP'] = int(row[4])
                    elif tile_count == 5:
                        player_stat['Physical attack'] = int(row[5])
                    elif tile_count == 6:
                        player_stat['Physical resistance'] = int(row[6])
                    elif tile_count == 7:
                        player_stat['Magical attack'] = int(row[7])
                    elif tile_count == 8:
                        player_stat['Magical resistance'] = int(row[8]) 
                    elif tile_count == 9:
                        player_stat['Speed'] = int(row[9])
                    tile_count += 1

            line_count += 1
        print(player) 
        print(player_stat)
        print(player['orientation'][0])

    return

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

    if player['position'][0] != 0 and player['position'][1] != 0:
        spawn_point = []
        spawn_point.append(player['position'][0])
        spawn_point.append(player['position'][1])
    return

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


    return

def movement_left():

    if camera_position[0] == 0 and player_position[0] <= screen_size[0] // 2:
        camera_position[0] = 0
        player_position[0] -= movement

    elif camera_position[0] ==  (((width) * tile_size) - screen_size[0]) and player_position[0] > screen_size[0] // 2:
        player_position[0] -= movement

    else:
        camera_position[0] -= movement
    

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

    return


### Action ###


def manage_game_keys(key):
    global player_position, camera_position, player, menu, game, game_menu, inventory, squad

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
        
        player['orientation'][0] = 4
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
        
        player['orientation'][0] = 2
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
        
        player['orientation'][0] = 3
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
        
        player['orientation'][0] = 1
        start_animation_front(now)
          
    elif key == pygame.K_ESCAPE:
        game_menu = True
        game = False

    elif key == pygame.K_i:
        game = False
        inventory = True
    
    elif key == pygame.K_u:
        game = False
        squad = True

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
    
    if type_key == 2:
        print(evenement.key)

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
    global cross_squad_color,game,squad, player_font_color,player_stat_display

    if type_key == -1:
        if rect_collide(cross_squad_rect,pygame.mouse.get_pos()):
            cross_squad_color = RED
        elif rect_collide(player_font_rect,pygame.mouse.get_pos()):
            player_font_color = RED
        else:
            cross_squad_color = BLACK
            player_font_color = PURPLE

    elif type_key == 2 and evenement.button == 1:
        if rect_collide(cross_squad_rect, pygame.mouse.get_pos()):
            squad = False
            game = True
        elif rect_collide(player_font_rect, pygame.mouse.get_pos()):
            player_stat_display = True
            squad = False

    elif type_key == 1:
        if evenement.key == pygame.K_u:
            squad = False
            game = True
    
    return

def manage_player_stat_keys(type_key,evenement):
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
            range_list.append('orientation')
            range_list.append(player['orientation'][0])
        elif j == 2:
            range_list.append('inventory')

            for i in range (0,inventory_size):
                range_list.append(player['inventory'][i])
        elif j == 3:
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
                    range_list.append(player_stat['Physical attack'])
                elif i == 5:
                    range_list.append(player_stat['Physical resistance'])
                elif i == 6:
                    range_list.append(player_stat['Magical attack'])
                elif i == 7:
                    range_list.append(player_stat['Magical resistance']) 
                elif i == 8:
                    range_list.append(player_stat['Speed'])

        field_list.append(range_list)
        range_list = []

    out = open("player/save1.csv",'w')
    outw = csv.writer(out)
    outw.writerows(field_list)
    out.close()
    return


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
        sprite = sprite_player[player['orientation'][0]]

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
    global cross_squad_rect,player_font_rect

    squad_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10 ,screen_size[0]// 10 * 8  ,screen_size[1]// 10 * 8)
    pygame.draw.rect(window,GREY,squad_first_rect)

    squad_rect = pygame.Rect(screen_size[0] // 10 + screen_size[0] // 200 * 3,screen_size[1] // 10 + screen_size[0] // 200 * 3 , screen_size[0]//10 * 8 - 2 * screen_size[0] // 200 * 3 ,screen_size[1]//10 * 8 - 2 *screen_size[0] // 200 * 3)
    pygame.draw.rect(window,LIGHT_GREY,squad_rect)

    squad_font = pygame.font.SysFont("monospace", 50, True)

    cross = squad_font.render("X", True, cross_squad_color)
    cross_size = squad_font.size("X")

    player_font = squad_font.render("Player", True, player_font_color)
    player_font_size = squad_font.size("Player")

    cross_first_rect = pygame.Rect(screen_size[0] // 10,screen_size[1] // 10, cross_size[0] + 7, cross_size[1] + 7)
    pygame.draw.rect(window,GREY,cross_first_rect)

    window.blit(cross,(screen_size[0] // 10 + 5 , screen_size[1] // 10 + 5))
    window.blit(player_font,(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2))

    cross_squad_rect = pygame.Rect(screen_size[0] // 10 + 5, screen_size[1] // 10 + 5,cross_size[0],cross_size[1])
    player_font_rect = pygame.Rect(screen_size[0] // 10 * 2 , screen_size[1] // 10 * 2,player_font_size[0],player_font_size[1])
    
    return

def display_stat_player():
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


### Calcul ###


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
    print("Orientation  : " + str(player['orientation'][0]))
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

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

create_player()
create_spawn_point()
define_spawn_point()

clock = pygame.time.Clock()

pygame.key.set_repeat(100,25)

create_field()
create_object()
create_collide()
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
        elif squad:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_squad_keys(2,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_squad_keys(1,evenement)


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


    elif squad:
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


    clock.tick(framerate)