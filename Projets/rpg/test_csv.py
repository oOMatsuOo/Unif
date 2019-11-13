import csv



with open("maps.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        character_count = 0
        while character_count < 7:
            print(f"{row[character_count]}", end=' ')
            character_count += 1
        line_count += 1
        print()
    print(f"Processed {line_count} lines")


def new_animation():
    return {
        'next_move_movement':None,
        'choreography':[]
    }
#
#def add_move(animation, move):
    animation['choreography'].append(move)
#
#def repete(animation, times):
    animation['repetition'] = times
    animation['loop'] = False
#
#def current_move(animation):
    if animation['index_move'] == None:
        return None
    else:
        return name_move(animation['choreography'][animation[index_move]])
        
#def animate(animation):
    if animation['index_move'] == None:
        start_animation(animation)
    elif animation['next_move_moment'] <= pygame.time.get_ticks():
        if animation['index_move'] == len(animation['choreography']) - 1:
            if animation['boucle']:
                start_animation(animation)
            else:
                if animation['repetion'] > 0:
                    animation['repetition'] -= 1
                    start_animation(animation)
                else:
                    stop_animation(animation)
        else:
            start_move(animation, animation['index_move'] + 1)
#
#def name_move(move):
    return move[0]
#
#def duration_move(move):
    return move[1]

#def create_player_sprite():
    global sprite_player,animation_front,animation_back,animation_right,animation_left

    sprite_player = {
            'front':{},
            'back':{},
            'right':{},
            'left':{}
            }

    for name_image, name_file in (('front_right','front_right.png'),
                                ('front_left','front_left.png'),
                                ('front_stand','front_stand.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (case_size,case_size))
        add_position(sprite_player['front'],name_image, image)

    animation_front = new_animation()
    add_move(animation_front, ('front_right', 80))
    add_move(animation_front, ('front_left', 80))

    for name_image, name_file in (('back_right','back_right.png'),
                                ('back_left','back_left.png'),
                                ('back_stand','back_stand.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (case_size,case_size))
        add_position(sprite_player['back'],name_image, image)

    animation_back = new_animation()
    add_move(animation_back, ('back_right', 80))
    add_move(animation_back, ('back_left', 80))

    for name_image, name_file in (('left_right','left_right.png'),
                                ('left_left','left_left.png'),
                                ('left_stand', 'left_stand.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (case_size,case_size))
        add_position(sprite_player['left'],name_image, image)

    animation_left = new_animation()
    add_move(animation_left, ('left_right', 80))
    add_move(animation_left, ('left_left', 80))

    for name_image, name_file in (('right_right','right_right.png'),
                                ('right_left','right_left.png'),
                                ('right_stand', 'right_stand.png')):
        path = 'pictures/player/' + name_file
        image = pygame.image.load(path).convert_alpha(window)
        image = pygame.transform.scale(image, (case_size,case_size))
        add_position(sprite_player['right'],name_image, image)

    animation_right = new_animation()
    add_move(animation_right, ('right_right', 80))
    add_move(animation_right, ('right_left', 80))

    return
