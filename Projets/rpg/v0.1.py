import csv
import pygame
import math
import sys
import subprocess

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

menu = True

game = False

option = False

screen_resolution_menu = False

control_menu = False

ratio = [9,16]

screen_size = [0,0]

width = 0
height= 0

framerate = 120
animation_duration = 150
is_animated = False
animation = 0

field = {}

player_position = [0, 0]
player_field_position = [0, 0]
camera_position = [0, 0]

middle = 0

collide = []

orientation = "front"

game_color = PURPLE
option_color = PURPLE
screen_resolution_color = PURPLE
control_color = PURPLE


### FUNCTION ###


### Screen ###


def define_screen_size(ratio):
    global screen_size, tile_size, movement,divide_tile

    different_screen_size = [426,640,768,800,848,896,960,1024,1152,1280,1366,1600,1920] 

    screen_size[0] = different_screen_size[12]
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

def define_spawn_point(point):
    global player_field_position,player_position,camera_position

    if point[1] <= screen_tile_size[1] // 2:
        player_position[1] = - point[1] * tile_size
        camera_position[1] = 0
    else:
        player_position[1] = - screen_tile_size[1] // 2 * tile_size
        camera_position[1] = - point[1] * tile_size + ( screen_tile_size[1] // 2 * tile_size)

    if point[0] <= screen_tile_size[0] // 2:
        player_position[0] = point[0] * tile_size
        camera_position[0] = 0
    else:
        player_position[0] = screen_tile_size[0] // 2 * tile_size
        camera_position[0] = point[0] * tile_size - screen_tile_size[0] // 2 * tile_size


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
    global player_position, camera_position, orientation, menu, game

    if key == pygame.K_LEFT or key == pygame.K_q: 
        if player_field_position[0] % tile_size == 0:
            if player_field_position[1] % tile_size == 0:
                if not field[-player_field_position[1] // tile_size][player_field_position[0] // tile_size - 1] in collide :
                    movement_left()
         
            else:
                if not field[-player_field_position[1] // tile_size][player_field_position[0] // tile_size - 1] in collide and not field[-player_field_position[1] // tile_size + 1][player_field_position[0]//tile_size - 1] in collide:
                    movement_left()

        else:
            movement_left()
        
        orientation = "left"
        start_animation_left(now)

    elif key == pygame.K_RIGHT or key == pygame.K_d:
        if player_field_position[0] % tile_size == 0:
            if player_field_position[1] % tile_size == 0:
                if not field[-player_field_position[1] // tile_size][player_field_position[0] // tile_size + 1] in collide :
                    movement_right()
            else:
                if not field[-player_field_position[1] // tile_size][player_field_position[0] // tile_size + 1] in collide and not field[-player_field_position[1] // tile_size + 1][player_field_position[0] // tile_size + 1] in collide:
                    movement_right()
        else:
            movement_right()
        
        orientation = "right"
        start_animation_right(now)
        
    elif key == pygame.K_UP or key == pygame.K_z:
        if player_field_position[1] % tile_size == 0:
            if player_field_position[0] % tile_size == 0:
                if not field[-player_field_position[1] // tile_size - 1][player_field_position[0] // tile_size] in collide :
                    movement_up()
                    
            else:
                if not field[-player_field_position[1] // tile_size - 1][player_field_position[0] // tile_size] in collide and not field[-player_field_position[1] // tile_size - 1][player_field_position[0] // tile_size + 1] in collide :
                    movement_up()

        else:
            movement_up()
        
        orientation = "back"
        start_animation_back(now)

    elif key == pygame.K_DOWN or key == pygame.K_s:
        if player_field_position[1] % tile_size == 0:
            if player_field_position[0] % tile_size == 0:
                if not field[-player_field_position[1] // tile_size + 1][player_field_position[0] // tile_size] in collide:
                    movement_down()
            else:
                if not field[-player_field_position[1] // tile_size + 1][player_field_position[0] // tile_size] in collide and not field[-player_field_position[1] // tile_size + 1][player_field_position[0] // tile_size + 1] in collide:
                    movement_down()
        else:
            movement_down()
        
        orientation = "front"
        start_animation_front(now)
          
    elif key == pygame.K_ESCAPE:
        menu = True
        game = False

    return

def manage_menu_keys(evenement):
    global game_color, option_color, menu, option, game

    if evenement == -1:
        if rect_collide(game_rect ,pygame.mouse.get_pos()):
            game_color = RED
        elif rect_collide(option_rect ,pygame.mouse.get_pos()):
            option_color = RED
        else:
            option_color = PURPLE
            game_color = PURPLE

    elif evenement.button == 1:
            if rect_collide(game_rect ,pygame.mouse.get_pos()):
                menu = False
                game = True
            elif rect_collide(option_rect ,pygame.mouse.get_pos()):
                menu = False
                option = True

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


### Visual ###


def add_position(entity,name,image):
    entity[name] = image

    return

def create_player_sprite():
    global sprite_player

    sprite_player = {}

    for name_image , name_file in (('front', 'front_stand.png'),
                                    ('back', 'back_stand.png'),
                                    ('right', 'right_stand.png'),
                                    ('left', 'left_stand.png')):
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

def display_player(time):

    if is_animated:
        if animation == 'left':
            if sprite_left['next_move_moment'] - animation_duration > time:
                sprite = sprite_left['choreography'][0][1]
            else:
                sprite = sprite_left['choreography'][1][1]
        elif animation == 'right':
            if sprite_right['next_move_moment'] - animation_duration > time:
                sprite = sprite_right['choreography'][0][1]
            else:
                sprite = sprite_right['choreography'][1][1]
        elif animation == 'front':
            if sprite_front['next_move_moment'] - animation_duration > time:
                sprite = sprite_front['choreography'][0][1]
            else:
                sprite = sprite_front['choreography'][1][1]
        elif animation == 'back':
            if sprite_back['next_move_moment'] - animation_duration > time:
                sprite = sprite_back['choreography'][0][1]
            else:
                sprite = sprite_back['choreography'][1][1]
    else :
        sprite = sprite_player[orientation]

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
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

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
    
    if not is_animated or animation != 'left':
        is_animated = True
        animation = 'left'
        sprite_left['next_move_moment'] = time + animation_duration * 2

    elif sprite_left['next_move_moment'] <= time:
        sprite_left['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_right(time):
    global is_animated, animation, sprite_right
    
    if not is_animated or animation != 'right':
        is_animated = True
        animation = 'right'
        sprite_right['next_move_moment'] = time + animation_duration * 2

    elif sprite_right['next_move_moment'] <= time:
        sprite_right['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_front(time):
    global is_animated, animation, sprite_front
    
    if not is_animated or animation != 'front':
        is_animated = True
        animation = 'front'
        sprite_front['next_move_moment'] = time + animation_duration * 2

    elif sprite_front['next_move_moment'] <= time:
        sprite_front['next_move_moment'] = time + animation_duration * 2
        
        return

def start_animation_back(time):
    global is_animated, animation, sprite_back
    
    if not is_animated or animation != 'back':
        is_animated = True
        animation = 'back'
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

def calcul_player_field_position():
    global player_field_position

    player_field_position[0] = player_position[0] + camera_position[0] 
    player_field_position[1] = player_position[1] + camera_position[1]

    return

def impress():
    print("CAM          : " + str(camera_position))
    print("PLAYER       : " + str(player_position))
    print("Screen size  : " + str(screen_size))
    print("tile size    : " + str(tile_size))
    print("Player field : " + str(player_field_position))
    print("Height       : " + str(height))
    print("Width        : " + str(width))
    print("Screen tile  : " + str(screen_tile_size))
    print("Collide      : " + str(collide))
    print("Orientation  : " + str(orientation))
    print("Move         : " + str(movement))
    print("Animated     : " + str(is_animated))
    print("")

    return

def whole_divisor(x,n):
    
    return x %  n == 0
    
def is_always_animated(time):
    global is_animated

    if is_animated:
        if animation == 'left':
            if sprite_left['next_move_moment'] < time:
                is_animated = False
        elif animation == 'back':
            if sprite_back['next_move_moment'] < time:
                is_animated = False
        elif animation == 'front':
            if sprite_front['next_move_moment'] < time:
                is_animated = False
        elif animation == 'right':
            if sprite_right['next_move_moment'] < time:
                is_animated = False



### GAME ###


pygame.init()

define_screen_size(ratio)
screen_tile_size = (pixel_to_coordinates(screen_size[0]), pixel_to_coordinates(screen_size[1]))
define_spawn_point((15,17))

window = pygame.display.set_mode(screen_size)
pygame.display.set_caption("First RPG")

clock = pygame.time.Clock()
background_color = GREY

pygame.key.set_repeat(50,50)

create_field()
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
                manage_menu_keys(evenement)
        elif option:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_option_keys(1,evenement)
            elif evenement.type == pygame.KEYDOWN:
                manage_option_keys(2,evenement)


    if menu:
        ### Menu

        window.fill(background_color)

        display_menu_screen()

        manage_menu_keys(-1)

        pygame.display.flip()
        

    elif game:
        ### Game
        
        stay_at_screen()

        calcul_player_field_position()

        impress()

        display_game_screen()

        display_player(now)

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