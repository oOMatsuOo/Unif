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

screen_size = (1000,800)

width = 36
height= 0

case_size = screen_size[0]//20

framerate = 60

field = {}

camera_position = [0, 0]

movement = case_size // 2

middle = 0

properties_width = 1

collide = []

orientation = "front"

game_color = PURPLE
menu_color = PURPLE


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

def movement_up():

    if camera_position[1] == 0 and player_position[0] >= -screen_size[1] // 2:
        camera_position[1] = 0
        player_position[1] += movement

    elif camera_position[1] == (-((height) * case_size) + screen_size[1]) and player_position[1] <= -screen_size[1] // 2:
        player_position[1] += movement

    else:
        camera_position[1] += movement
    

    return

def movement_down():

    if camera_position[1] == 0 and player_position[1] >= -screen_size[1] // 2:
        camera_position[1] = 0
        player_position[1] -= movement

    elif camera_position[1] == (-((height) * case_size) + screen_size[1]) and player_position[1] <= screen_size[1] // 2:
        camera_position[1] = (-((height) * case_size) + screen_size[1])
        player_position[1] -= movement

    else:
        camera_position[1] -= movement


    return

def movement_left():

    if camera_position[0] == 0 and player_position[0] <= screen_size[0] // 2:
        camera_position[0] = 0
        player_position[0] -= movement

    elif camera_position[0] ==  (((width) * case_size) - screen_size[0]) and player_position[0] > screen_size[0] // 2:
        player_position[0] -= movement

    else:
        camera_position[0] -= movement
    

    return

def movement_right():

    if camera_position[0] == 0 and player_position[0] < screen_size[0] // 2:
        camera_position[0] = 0
        player_position[0] += movement

    elif camera_position[0] >= (((width) * case_size) - screen_size[0]) and player_position[0] >= screen_size[0] // 2:
        camera_position[0] = (((width) * case_size) - screen_size[0])
        player_position[0] += movement

    else:
        camera_position[0] += movement

    return


### Action ###


def manage_game_keys(key):
    global player_position, camera_position, orientation

    if key == pygame.K_LEFT: 
        if player_field_position[0] % case_size == 0:
            if player_field_position[1] % case_size == 0:
                if not field[-player_field_position[1] // case_size][player_field_position[0]//case_size - 1] in collide :
                    movement_left()
            else:
                if not field[-player_field_position[1] // case_size][player_field_position[0]//case_size - 1] in collide and not field[-player_field_position[1] // case_size + 1][player_field_position[0]//case_size - 1] in collide:
                    movement_left()
        else:
            movement_left()
        
        orientation = "left"

    elif key == pygame.K_RIGHT:
        if player_field_position[0] % case_size == 0:
            if player_field_position[1] % case_size == 0:
                if not field[-player_field_position[1] // case_size][player_field_position[0] // case_size + 1] in collide :
                    movement_right()
            else:
                if not field[-player_field_position[1] // case_size][player_field_position[0] // case_size + 1] in collide and not field[-player_field_position[1] // case_size + 1][player_field_position[0] // case_size + 1] in collide:
                    movement_right()
        else:
            movement_right()
        
        orientation = "right"
        

    elif key == pygame.K_UP:
        if player_field_position[1] % case_size == 0:
            if player_field_position[0] % case_size == 0:
                if not field[-player_field_position[1] // case_size - 1][player_field_position[0] // case_size] in collide :
                    movement_up()
                    
            else:
                if not field[-player_field_position[1] // case_size - 1][player_field_position[0] // case_size] in collide and not field[-player_field_position[1] // case_size - 1][player_field_position[0] // case_size + 1] in collide :
                    movement_up()

        else:
            movement_up()
        
        orientation = "back"

    elif key == pygame.K_DOWN:
        if player_field_position[1] % case_size == 0:
            if player_field_position[0] % case_size == 0:
                if not field[-player_field_position[1] // case_size + 1][player_field_position[0] // case_size] in collide:
                    movement_down()
            else:
                if not field[-player_field_position[1] // case_size + 1][player_field_position[0] // case_size] in collide and not field[-player_field_position[1] // case_size + 1][player_field_position[0] // case_size + 1] in collide:
                    movement_down()
        else:
            movement_down()
        
        orientation = "front"
          
    return

def manage_menu_keys(key):
    
    print(key)
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
        image = pygame.transform.scale(image, (case_size,case_size))
        add_position(sprite_player,name_image,image)

def display_player():

    sprite = sprite_player[orientation]

    window.blit(sprite,(player_position[0],-player_position[1]))

    return

def display_game_screen():
    height_screen = screen_size[1]//case_size
    width_screen = screen_size[0]//case_size

    camera_case_Y = -camera_position[1] // case_size
    camera_case_X = camera_position[0] // case_size

    i = camera_case_Y
    i_prime = (camera_position[1]/case_size % 1)
    borne_i = height_screen + camera_case_Y

    j_first = (camera_position[0]/case_size % 1)
    borne_j = width_screen + camera_case_X 
    
    if i_prime % 1 != 0:
        i_prime = -1 + i_prime
        borne_i = height_screen + camera_case_Y + 1


    if j_first % 1 != 0:
        j_first = - j_first
        borne_j = width_screen + camera_case_X + 1


    while i < borne_i :
        j = camera_case_X
        j_prime = j_first
        while j <  borne_j:
            create_case(field[i][j], j_prime, i_prime)
            j += 1
            j_prime += 1

        i += 1
        i_prime += 1

    return

def display_menu_screen():
    
    menu_font = pygame.font.SysFont("monospace", 100, True)
    list_font = pygame.font.SysFont("monospace", 50, True)

    menu = menu_font.render("MENU", True, ORANGE)
    menu_size = menu_font.size("MENU")
    game = list_font.render("Game", True, game_color)
    option = list_font.render("Option",True,option_color)

    window.blit(menu, (screen_size[0] // 2 - menu_size[0] // 2,screen_size[1]//10))
    window.blit(game,(screen_size[0] // 5, screen_size[1] // 9 * 3))
    window.blit(option,(screen_size[0] // 5, screen_size[1] // 9 * 4))


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
    print("Case size    : " + str(case_size))
    print("Player field : " + str(player_field_position))
    print("Height       : " + str(height * case_size))
    print("Width        : " + str(width * case_size))
    print("Screen case  : " + str(screen_case_size))
    print("Collide      : " + str(collide))
    print("Orientation  : " + str(orientation))
    print("Move         : " + str(movement))
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
create_player_sprite()

screen_case_size = (pixel_to_coordinates(screen_size[0]), pixel_to_coordinates(screen_size[1]))
player_position = [case_size * 10, -case_size * 9]
player_field_position = [player_position[0], player_position[1]]

create_player_sprite()

while open_game:
    now = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif game:
            if evenement.type == pygame.KEYDOWN:
                manage_game_keys(evenement.key)
        elif menu:
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                manage_menu_keys(evenement.key)
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_LEFT:
                    menu = False
                    game = True

    if menu:
        ### Menu

        display_menu_screen()
        pygame.display.flip()
        

    if game:
        ### Game
        
        stay_at_screen()

        calcul_player_field_position()

        impress()

        display_game_screen()

        display_player()

        pygame.display.flip()


    if option:
        ### Option
        print("")

    clock.tick(framerate)