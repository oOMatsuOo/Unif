import pygame
import math
import random

# Kieran Van Muysewinkel
# Saïd Hormat-Allah

H = 0
V = 1

BLEU = (0, 0, 255)
BORDEAU = (176, 29, 29)
BLEU_CLAIR = (0, 191, 200)
JAUNE = (255, 255, 0)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BALLE_RAYON = 10
BALLE_DIAM = 2 *BALLE_RAYON

BRIQUE_LARGEUR = 200
BRIQUE_HAUTEUR = 30

RAQUETTE_LARGEUR = 70
RAQUETTE_HAUTEUR = 10
RAQUETTE_ESPACE = 10
RAQUETTE_DEPLACEMENT = 10
RAQUETTE_ZONES = 4

TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT

VERS_DROITE = 1
VERS_GAUCHE = -1

MUR_EPAISSEUR = 10

CENTRE = 0
GAUCHE = 1
DROITE = 2
DESSUS = 4
HAUT_GAUCHE = 5
HAUT_DROITE = 6
DESSOUS = 8
DESSOUS_GAUCHE = 9
DESSOUS_DROITE = 10

VITESSE_MAX = BALLE_RAYON
AMPLI_VITESSE_INIT = 5
FACTEUR_AUGMENTATION_VITESSE = 1.1
FRAPPES_AUGMENTATION_VITESSE = 4


# --- Définitions de fonctions
def deplace_raquette(sens):
    raquette_position[H] += RAQUETTE_DEPLACEMENT * sens
    test_touche_gauche(raquette_position, 0, MUR_EPAISSEUR)
    test_touche_droite(raquette_position, RAQUETTE_LARGEUR, FENETRE_LARGEUR-MUR_EPAISSEUR)


def test_touche_db(objet, distance, point, direction, separe):
    if objet[direction] + distance >= point:
        if separe:
            objet[direction] = point - distance
        return True
    else:
        return False


def test_touche_gh(objet, distance, point, direction, separe):
    if objet[direction] - distance <= point:
        if separe:
            objet[direction] = point + distance
        return True
    else:
        return False


def test_touche_droite(objet, largeur_droite, point_droit, separe=True):
    return test_touche_db(objet, largeur_droite, point_droit, H, separe)


def test_touche_gauche(objet, largeur_gauche, point_gauche, separe=True):
    return test_touche_gh(objet, largeur_gauche, point_gauche, H, separe)


def test_touche_haut(objet, hauteur_haut, point_haut, separe=True):
    return test_touche_gh(objet, hauteur_haut, point_haut, V, separe)


def test_touche_bas(objet, hauteur_bas, point_bas, separe=True):
    return test_touche_db(objet, hauteur_bas, point_bas, V, separe)


def traite_entrees():
    global fini
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == TOUCHE_DROITE:
                deplace_raquette(VERS_DROITE)
            elif evenement.key == TOUCHE_GAUCHE:
                deplace_raquette(VERS_GAUCHE)


def anime():
    global fini
    balle_position[H] = balle_position[H] + balle_vitesse[H]
    balle_position[V] = balle_position[V] + balle_vitesse[V] 

    if test_touche_droite(balle_position, BALLE_RAYON, FENETRE_LARGEUR) \
       or test_touche_gauche(balle_position, BALLE_RAYON, MUR_EPAISSEUR):
        change_vitesse(H, -vitesse_direction[H])
    
    if test_touche_haut(balle_position, BALLE_RAYON, MUR_EPAISSEUR):
        change_vitesse(V, -vitesse_direction[V])
     
    test_collision((brique_position, (BRIQUE_LARGEUR, BRIQUE_HAUTEUR)))
    
    test_collision((raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))

    if test_touche_bas(balle_position, BALLE_RAYON, FENETRE_HAUTEUR + BALLE_DIAM):
        fini = True

def dessine_court():
    fenetre.fill(BLEU_CLAIR)
    marquoir = police.render(str(score), True, BLEU)
    fenetre.blit(marquoir, (5 * FENETRE_LARGEUR // 8, FENETRE_HAUTEUR // 10))
    pygame.draw.rect(fenetre, BLANC, ((0,0), (MUR_EPAISSEUR, FENETRE_HAUTEUR)))
    int_balle_position = (int(balle_position[H]), int(balle_position[V]))
    print(balle_vitesse)
    pygame.draw.rect(fenetre, BLANC, ((MUR_EPAISSEUR, 0), (FENETRE_LARGEUR - 2 * MUR_EPAISSEUR, MUR_EPAISSEUR)))
    pygame.draw.rect(fenetre, BLANC, ((FENETRE_LARGEUR - MUR_EPAISSEUR, 0), (MUR_EPAISSEUR, FENETRE_HAUTEUR)))
    pygame.draw.circle(fenetre, JAUNE, int_balle_position, BALLE_RAYON)
    pygame.draw.rect(fenetre, ROUGE, (raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))
    pygame.draw.rect(fenetre, BORDEAU, (brique_position, (BRIQUE_LARGEUR, BRIQUE_HAUTEUR)))

def distance2(pt1, pt2):
    delta_h = pt1[H] - pt2[H]
    delta_v = pt1[H] - pt2[H]
    return delta_h * delta_h + delta_v * delta_v

def position_horizontale_rel(rect):
    if balle_position[H] < rect[0][H]:
        return GAUCHE
    elif balle_position[H] > rect[0][H] + rect[1][H]:
        return DROITE
    else : 
        return CENTRE

def position_verticale_rel(rect):
    if balle_position[V] < rect[0][V]:
        return DESSUS
    elif balle_position[V] > rect[0][V] + rect[1][V]:
        return DESSOUS
    else :
        return CENTRE

def position_relative(rect):
    return position_horizontale_rel(rect) + position_verticale_rel(rect)

def test_collision(rect):
    global score
    global brique_position
    ball_rect = pygame.Rect((balle_position[H] - BALLE_RAYON, balle_position[V] - BALLE_RAYON), (BALLE_DIAM, BALLE_DIAM))
    if ball_rect.colliderect(rect):
        if rect[0] == brique_position:
            augmente_score()
            x = random.randint(200, FENETRE_LARGEUR-200)
            y = random.randint(200,FENETRE_HAUTEUR-200)
            brique_position = (x,y)
        rayon2 = BALLE_RAYON * BALLE_RAYON
        position = position_relative(rect)
        if position == GAUCHE:
            if test_touche_droite(balle_position, BALLE_RAYON, rect[0][H]):
                change_vitesse(H, -abs(vitesse_direction[H]))
        elif position == DROITE:
            if test_touche_gauche(balle_position, BALLE_RAYON, rect[0][H] + rect[1][H]):
                change_vitesse(H, abs(vitesse_direction[H]))
        elif position ==  DESSUS:
            if test_touche_bas(balle_position, BALLE_RAYON, rect[0][V]):
                if rect[0] == brique_position:
                     change_vitesse(V, -vitesse_direction[V])
                else:
                    zone = zone_raquette (balle_position[H])
                    change_vitesse(H, RAQUETTE_VITESSE_REBOND[zone][H])
                    change_vitesse(V, RAQUETTE_VITESSE_REBOND[zone][V])
        elif position == DESSOUS:
            if test_touche_haut(balle_position, BALLE_RAYON, rect[0][V] + rect[1][V]):
                change_vitesse(V, -vitesse_direction[V])
        elif position == HAUT_GAUCHE:
            if distance2(balle_position, rect[0]) <= rayon2:
                collision_coin_haut_gauche(rect)
        elif position == HAUT_DROITE:
            if distance2(balle_position, (rect[0][H] + rect[1][H], rect[0][V])) <= rayon2:
               collision_coin_haut_droite(rect)
        elif position == DESSOUS_GAUCHE:
            if distance2(balle_position, (rect[0][H], rect[0][V] + rect[1][V])) <= rayon2:
                collision_coin_bas_gauche(rect)
        elif position == DESSOUS_DROITE:
            if distance2(balle_position, (rect[0][H] + rect[1][H], rect[0][V] + rect[1][V])) <= rayon2:
                collision_coin_bas_droite(rect)
        else:
            # Cas final: CENTRE. On fait l'hypothèse que l'amplitude de la vitesse ne dépasse jamais la taille du rayon.
            # Il faudra s'assurer que cette condition est toujours vraie.
            # Eviter un recouvrement lorsque raquette et balle bougent l'une vers l'autre:
            delta_g = abs(balle_position[H] - rect[0][H])
            delta_d = abs(balle_position[H] - rect[0][H] - rect[1][H])
            if delta_g < delta_d:
                balle_position[H] = rect[0][H] - BALLE_RAYON
                change_vitesse(H, -abs(vitesse_direction[H]))
            else:
                balle_position[H] = rect[0][H] + rect[1][H] + BALLE_RAYON
                change_vitesse(H, abs(vitesse_direction[H]))

def augmente_score():
    global score, vitesse_amplitude, balle_vitesse

    score += 1
    if vitesse_amplitude < VITESSE_MAX and score % FRAPPES_AUGMENTATION_VITESSE == 0:
        vitesse_amplitude = min(vitesse_amplitude * FACTEUR_AUGMENTATION_VITESSE, VITESSE_MAX)
        balle_vitesse = vitesse()

def resoudre_collision_coin(coin, delta_h, delta_v, vitesse_h, vitesse_v):
    global balle_vitesse

    balle_vitesse = vitesse_h, vitesse_v

    balle_position[H] = coin[H] + delta_h
    balle_position[V] = coin[V] + delta_v

def collision_coin_haut_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    vitesse_rebond = vitesse_coin(VERS_GAUCHE)
    print(vitesse_rebond)
    resoudre_collision_coin(rect[0], -delta, -delta, vitesse_rebond[H], vitesse_rebond[V])


def collision_coin_haut_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    vitesse_rebond = vitesse_coin(VERS_DROITE)
    resoudre_collision_coin((rect[0][H] + rect[1][H], rect[0][V]), delta, -delta, vitesse_rebond[H],vitesse_rebond[V])


def collision_coin_bas_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H], rect[0][V] + rect[1][V]), -delta, delta, -abs(balle_vitesse[H]), abs(balle_vitesse[V]))


def collision_coin_bas_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H] + rect[1][H], rect[0][V] + rect[1][V]), delta, delta, abs(balle_vitesse[H]), abs(balle_vitesse[V]))

def change_vitesse(composante, val):
    global balle_vitesse

    vitesse_direction[composante] = val
    balle_vitesse = vitesse()

def vitesse():
    return (round(vitesse_amplitude * vitesse_direction[H]), round(vitesse_amplitude * vitesse_direction[V]))

def vecteur_unitaire(angle):
    angle_radian = math.radians(angle)
    return(math.cos(angle_radian), math.sin(angle_radian))

def zone_raquette(position_horizontale):
    x_relatif = position_horizontale - raquette_position[H]
    if x_relatif < 0 or x_relatif >= RAQUETTE_LARGEUR:
        return -1
    return int(x_relatif // RAQUETTE_LARGEUR * RAQUETTE_ZONES)

def vitesse_coin(cote):
    if cote == VERS_DROITE:
        v = RAQUETTE_REBOND_COIN[2:]
    else:
        v = RAQUETTE_REBOND_COIN[:2]
    return random.choice(v)


pygame.init()
pygame.key.set_repeat(200, 25)

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(BLEU_CLAIR)

balle_position = [250, 150]
vitesse_direction = [math.sqrt(0.5), math.sqrt(0.5)]
vitesse_amplitude = AMPLI_VITESSE_INIT
balle_vitesse = vitesse()

RAQUETTE_VITESSE_REBOND = tuple(vecteur_unitaire(a) for a in(-120,-100,-80,-60))
RAQUETTE_REBOND_COIN = tuple(vecteur_unitaire(a) for a in(-135,135,-45,45))

#brique_position = [FENETRE_LARGEUR // 2 - BRIQUE_LARGEUR // 2, FENETRE_HAUTEUR // 2]
# position de la brique
brique_position = [300,200]

raquette_position = [FENETRE_LARGEUR // 2 - RAQUETTE_LARGEUR // 2, FENETRE_HAUTEUR - RAQUETTE_ESPACE - RAQUETTE_HAUTEUR]

police = pygame.font.SysFont('monospace', FENETRE_HAUTEUR//12, True)

score = 0

fini = False
temps = pygame.time.Clock()

# --- Boucle principale
while not fini:
    # --- Traiter entrées joueur
    traite_entrees()

    # --- Logique du jeu
    anime()

    # --- Dessiner l'écran
    dessine_court()

    # --- Afficher (rafraîchir) l'écran
    pygame.display.flip()

    # --- 50 images par seconde
    temps.tick(50)

pygame.display.quit()
pygame.quit()