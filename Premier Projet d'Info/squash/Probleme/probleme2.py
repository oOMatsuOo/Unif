import pygame
import math
import random
import time

H = 0
V = 1

BLEU_CLAIR = (  0, 191, 200)
JAUNE      = (255, 255,   0)
ROUGE      = (255,   0,   0)
BLANC      = (255, 255, 255)
BLEU       = (  0,   0, 255)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BALLE_RAYON = 10
BALLE_DIAM = 2 * BALLE_RAYON

RAQUETTE_LARGEUR = 70
RAQUETTE_HAUTEUR = 10
RAQUETTE_ESPACE = 10
RAQUETTE_DEPLACEMENT = 10
RAQUETTE_ZONES = 4

TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT
TOUCHE_DROITE2 = pygame.K_s
TOUCHE_GAUCHE2 = pygame.K_a
TOUCHE_PAUSE  = pygame.K_p
TOUCHE_QUITTE = pygame.K_q

BOUTON_SOURIS_GAUCHE = 1

VERS_DROITE = 1
VERS_GAUCHE = -1

MUR_EPAISSEUR = 10

CENTRE         = 0
GAUCHE         = 1
DROITE         = 2
DESSUS         = 4
HAUT_GAUCHE    = 5
HAUT_DROITE    = 6
DESSOUS        = 8
DESSOUS_GAUCHE = 9
DESSOUS_DROITE = 10

VITESSE_MAX = BALLE_RAYON
AMPLI_VITESSE_INIT = 5
FACTEUR_AUGMENTATION_VITESSE = 1.1
FRAPPES_AUGMENTATION_VITESSE = 7

ancien_score = 0
BONUS = 2
SCORE_BONUS = 5
BONUS_DONNE = False

MAX_VIES = 3

# --- Définitions de fonctions
def deplace_raquette(sens):
    raquette_position[H] += RAQUETTE_DEPLACEMENT * sens
    test_touche_gauche(raquette_position, 0, MUR_EPAISSEUR)
    test_touche_droite(raquette_position, RAQUETTE_LARGEUR, FENETRE_LARGEUR - MUR_EPAISSEUR)

def souris_cliquee(pos):
    global score
    if distance2(pos, balle_position) > BALLE_RAYON * BALLE_RAYON:
        score = score // 2
    else:
        score = score * 2

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
    global fini, vies_restantes, pause, joue

    for evenement in pygame.event.get():
        if delai:
            return
        if evenement.type == pygame.QUIT:
            fini = True
            vies_restantes = 0
            joue = False
        elif evenement.type == pygame.KEYDOWN:
            if vies_restantes == 0: # Ecran intro
                if evenement.key == TOUCHE_QUITTE:
                    joue = False
                    fini = True
                else: # Toute touche (sauf Q) commence le jeu
                    vies_restantes = MAX_VIES
            else:
                if (evenement.key == TOUCHE_DROITE or evenement.key == TOUCHE_DROITE2) and not pause:
                    deplace_raquette(VERS_DROITE)
                elif (evenement.key == TOUCHE_GAUCHE or evenement.key == TOUCHE_GAUCHE2) and not pause:
                    deplace_raquette(VERS_GAUCHE)
                elif evenement.key == TOUCHE_PAUSE:
                    pause = not pause
                elif evenement.key == TOUCHE_QUITTE:
                    fini = True
                    vies_restantes = 0
        elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == BOUTON_SOURIS_GAUCHE and not pause :
            souris_cliquee(evenement.pos)

def anime():
    global fini, vies_restantes, ancien_score, RAQUETTE_LARGEUR, BONUS_DONNE
    balle_position[H] = balle_position[H] + balle_vitesse[H]
    balle_position[V] = balle_position[V] + balle_vitesse[V]

    if test_touche_droite(balle_position, BALLE_RAYON, FENETRE_LARGEUR - MUR_EPAISSEUR) \
       or test_touche_gauche(balle_position, BALLE_RAYON, MUR_EPAISSEUR):
        change_vitesse(H, -vitesse_direction[H])

    if test_touche_haut(balle_position, BALLE_RAYON, MUR_EPAISSEUR):
        change_vitesse(V, -vitesse_direction[V])

    if (score-ancien_score) >= SCORE_BONUS and not BONUS_DONNE:
        RAQUETTE_LARGEUR * BONUS
        BONUS_DONNE = True

    test_collision((raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))

    if test_touche_bas(balle_position, BALLE_RAYON, FENETRE_HAUTEUR + BALLE_DIAM):
        ancien_score = score
        if BONUS_DONNE:
            RAQUETTE_LARGEUR //= 2
            BONUS_DONNE = False
        fini = True
        vies_restantes -= 1


def dessine_court():
    fenetre.fill(BLEU_CLAIR)
    marquoir = police.render(str(score), True, BLEU)
    fenetre.blit(marquoir, (5 * FENETRE_LARGEUR // 8, FENETRE_HAUTEUR // 10))
    pygame.draw.rect(fenetre, BLANC, ((0, 0), (MUR_EPAISSEUR, FENETRE_HAUTEUR)))
    pygame.draw.rect(fenetre, BLANC, ((MUR_EPAISSEUR, 0), (FENETRE_LARGEUR - 2 * MUR_EPAISSEUR, MUR_EPAISSEUR)))
    pygame.draw.rect(fenetre, BLANC, ((FENETRE_LARGEUR - MUR_EPAISSEUR, 0), (MUR_EPAISSEUR, FENETRE_HAUTEUR)))
    for vies in range(vies_restantes - 1):
        pygame.draw.circle(fenetre, BLEU, (3 * FENETRE_LARGEUR // 8 + vies * MUR_EPAISSEUR + 2, MUR_EPAISSEUR // 2 ), (MUR_EPAISSEUR - 2) // 2)
    pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
    pygame.draw.rect(fenetre, ROUGE, (raquette_position, (RAQUETTE_LARGEUR, RAQUETTE_HAUTEUR)))
    if vies_restantes == 0:
        message = police.render("Au revoir...", True, JAUNE)
        message_largeur, message_hauteur = police.size("Au revoir...",)
        fenetre.blit(message, ((FENETRE_LARGEUR - message_largeur) // 2, 4 * FENETRE_HAUTEUR // 5))
    if pause:
        pygame.draw.rect(fenetre, BLANC, ((FENETRE_LARGEUR//2 - 35, FENETRE_HAUTEUR//2 - 25), (30, 50)))
        pygame.draw.rect(fenetre, BLANC, ((FENETRE_LARGEUR//2 + 5, FENETRE_HAUTEUR//2 - 25), (30, 50)))


def dessine_intro():
    fenetre.fill(BLEU_CLAIR)
    titre = police_titre.render('Squash!', True, JAUNE)
    titre_largeur, titre_hauteur = police_titre.size('Squash!')
    fenetre.blit(titre, ((FENETRE_LARGEUR - titre_largeur) // 2, (FENETRE_HAUTEUR - titre_hauteur) // 4))
    message1 = police.render("[Q]uitter", True, BLEU)
    message1_largeur, message1_hauteur = police.size("[Q]quitter")
    fenetre.blit(message1, ((FENETRE_LARGEUR - message1_largeur) // 2, 4 * FENETRE_HAUTEUR  // 5))
    message2 = police.render("N'importe quelle touche pour commencer...", True, BLEU)
    message2_largeur, message2_hauteur = police.size("N'importe quelle touche pour commencer...")
    fenetre.blit(message2, ((FENETRE_LARGEUR - message2_largeur) // 2, 4 * FENETRE_HAUTEUR // 5 + 1.2 * message1_hauteur))

def distance2(pt1, pt2):
    delta_h = pt1[H] - pt2[H]
    delta_v = pt1[V] - pt2[V]
    return delta_h * delta_h + delta_v * delta_v


# rect represente un rectangle ((gauche, haut), (largeur, hauteur))
def position_horizontale_rel(rect):
    if balle_position[H] < rect[0][H]:
        return GAUCHE
    elif balle_position[H] > rect[0][H] + rect[1][H]:
        return DROITE
    else:
        return CENTRE


# rect represente un rectangle ((gauche, haut), (largeur, hauteur))
def position_verticale_rel(rect):
    if balle_position[V] < rect[0][V]:
        return DESSUS
    elif balle_position[V] > rect[0][V] + rect[1][V]:
        return DESSOUS
    else:
        return CENTRE


# rect represente un rectangle ((gauche, haut), (largeur, hauteur))
def position_relative(rect):
    return position_horizontale_rel(rect) + position_verticale_rel(rect)


# rect represente un rectangle ((gauche, haut), (largeur, hauteur))
def test_collision(rect):
    ball_rect = pygame.Rect((balle_position[H] - BALLE_RAYON, balle_position[V] - BALLE_RAYON), (BALLE_DIAM, BALLE_DIAM))
    if ball_rect.colliderect(rect):
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
                zone = zone_raquette(balle_position[H])
                change_vitesse(H, RAQUETTE_VITESSE_REBOND[zone][H])
                change_vitesse(V, RAQUETTE_VITESSE_REBOND[zone][V])
                augmente_score()
        elif position == DESSOUS:
            if test_touche_haut(balle_position, BALLE_RAYON, rect[0][V] + rect[1][V]):
                change_vitesse(V, -vitesse_direction[V])
        elif position == HAUT_GAUCHE:
            if distance2(balle_position, rect[0]) <= rayon2:
                collision_coin_haut_gauche(rect)
                augmente_score()
        elif position == HAUT_DROITE:
            if distance2(balle_position, (rect[0][H] + rect[1][H], rect[0][V])) <= rayon2:
               collision_coin_haut_droite(rect)
               augmente_score()
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


def vitesse_coin(cote):
    if cote == VERS_DROITE:
        v = RAQUETTE_REBOND_COIN[2:]
    else:
        v = RAQUETTE_REBOND_COIN[:2]
    return random.choice(v)


def resoudre_collision_coin(coin, delta_h, delta_v, vitesse_h, vitesse_v):
    balle_position[H] = coin[H] + delta_h
    balle_position[V] = coin[V] + delta_v
    change_vitesse(H, vitesse_h)
    change_vitesse(V, vitesse_v)


def collision_coin_haut_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    vitesse_rebond = vitesse_coin(VERS_GAUCHE)
    resoudre_collision_coin(rect[0], -delta, -delta, vitesse_rebond[H], vitesse_rebond[V])


def collision_coin_haut_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    vitesse_rebond = vitesse_coin(VERS_DROITE)
    resoudre_collision_coin((rect[0][H] + rect[1][H], rect[0][V]), delta, -delta, vitesse_rebond[H], vitesse_rebond[V])


def collision_coin_bas_gauche(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H], rect[0][V] + rect[1][V]), -delta, delta, -abs(vitesse_direction[H]), abs(vitesse_direction[V]))


def collision_coin_bas_droite(rect):
    delta = round(BALLE_RAYON * 0.707)
    resoudre_collision_coin((rect[0][H] + rect[1][H], rect[0][V] + rect[1][V]), delta, delta, abs(vitesse_direction[H]), abs(vitesse_direction[V]))

def change_vitesse(composante, val):
    global balle_vitesse

    vitesse_direction[composante] = val
    balle_vitesse = vitesse()

def vitesse():
    return (round(vitesse_amplitude * vitesse_direction[H]), round(vitesse_amplitude * vitesse_direction[V]))


def vecteur_unitaire(angle):
    angle_radian = math.radians(angle)
    return (math.cos(angle_radian), math.sin(angle_radian))


def zone_raquette(position_horizontale):
    x_relatif = position_horizontale - raquette_position[H]
    if x_relatif < 0 or x_relatif >= RAQUETTE_LARGEUR:
        return -1
    return int(x_relatif / RAQUETTE_LARGEUR * RAQUETTE_ZONES)


random.seed()

pygame.init()
pygame.key.set_repeat(200, 25)

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(BLEU_CLAIR)

RAQUETTE_VITESSE_REBOND = tuple(vecteur_unitaire(a) for a in (-120, -100, -80, -60))
RAQUETTE_REBOND_COIN = tuple(vecteur_unitaire(a) for a in (-135, 135, -45, 45))

police = pygame.font.SysFont('monospace', FENETRE_HAUTEUR//20, True)
police_titre = pygame.font.SysFont('monospace', 80, True)

temps = pygame.time.Clock()

vies_restantes = 0
pause = False
joue   = True

# --- Boucle principale
while joue:
    delai = False
    balle_position = [FENETRE_LARGEUR // 2, FENETRE_HAUTEUR // 3]
    vitesse_direction = [math.sqrt(0.5), math.sqrt(0.5)]
    vitesse_amplitude = AMPLI_VITESSE_INIT
    balle_vitesse = vitesse()
    raquette_position = [FENETRE_LARGEUR // 2 - RAQUETTE_LARGEUR // 2,
                         FENETRE_HAUTEUR - RAQUETTE_ESPACE - RAQUETTE_HAUTEUR]
    score = 0

    traite_entrees()
    dessine_intro()
    pygame.display.flip()
    temps.tick(4)

    # --- Boucle partie
    while vies_restantes > 0:

        balle_position[V] = FENETRE_HAUTEUR // 3
        start = time.time()
        auto_pause = True
        fini = False
        delai = False

        while not fini:
            # --- Traiter entrées joueur
            traite_entrees()

            # --- Logique du jeu
            if not auto_pause and not pause and not delai:
                anime()
                if fini and vies_restantes == 0:
                    delai = True
                    fini = False
                    start = time.time()
            else:
                auto_pause = time.time() - start < 2.0
                if delai and not auto_pause:
                    fini = True

            # --- Dessiner l'écran
            dessine_court()

            # --- Afficher (rafraîchir) l'écran
            pygame.display.flip()

            # --- 50 images par seconde
            temps.tick(50)

pygame.display.quit()
exit()