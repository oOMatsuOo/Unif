import math
import pygame
import sys

# Constantes

NOIR   = (  0,  0,  0)
ROUGE  = (139,  0,  0)
VIOLET = (148,  0,211)
GRIS   = (105,105,105)
ORANGE = (255,140,  0)

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

position_vaisseau = ([400, 300])
orientation = 0

compteur_propulseur = 0

masse = 1
force_poussee = 0

marge_ecran = 50


# Fonctions


def afficher_vaisseau(position, angle):
    pi = math.pi

    global compteur_propulseur

    p = position
    r = 23
    a = angle 
    b = pi / 7
    rayon = 15

    if compteur_propulseur != 0:    # Affiche Flammes
        dessiner_triangle(ROUGE, p, 38, (a + pi + 21 * pi / 20), (pi / 30))
        dessiner_triangle(ROUGE, p, 38, (a + pi + 19 * pi / 20), (pi / 30))

    dessiner_triangle(ORANGE, p, r, a, b)   # Affiche orientation

    pygame.draw.circle(fenetre, GRIS, p, rayon)  # Affiche vaisseau


def dessiner_triangle(couleur, position, longueur, orientation, angle_interne):
    p = position
    r = longueur
    a = orientation
    b = angle_interne

    xp, yp = p

    p1 = [xp - (r * math.cos(a - b)), yp - (r * math.sin(a - b))]
    p2 = [xp - (r * math.cos(a + b)), yp - (r * math.sin(a + b))]

    triangle = [p, p1, p2]

    pygame.draw.polygon(fenetre, couleur, triangle)  

    return


def gerer_touche(touche):
    pi = math.pi
    global orientation, compteur_propulseur, force_poussee

    if touche == pygame.K_LEFT:
        orientation -= pi / 20
    elif touche == pygame.K_RIGHT:
        orientation += pi / 20
    elif touche == pygame.K_UP:
        compteur_propulseur += 3
        force_poussee = 0.0003


def initialiser_calculs():

    global Temps_debut, VX, VY,PX, PY, position_vaisseau

    Temps_debut = 0
    PX = float(position_vaisseau[0])
    PY = float(position_vaisseau[1])
    VX = float(0)
    VY = float(0)

    return


def mettre_a_jour_position():

    global Temps_debut, VX, VY, PX, PY, position_vaisseau, masse, force_poussee, orientation

    temps_maintenant = pygame.time.get_ticks()

    delta_temps = temps_maintenant - Temps_debut

    X = position_vaisseau[0]
    Y = position_vaisseau[1]

    a = force_poussee / masse

    ax = math.cos(orientation) * a
    ay = math.sin(orientation) * a

    VX += ax * delta_temps
    VY += ay * delta_temps

    X = VX * delta_temps + X
    Y = VY * delta_temps + Y

    position_vaisseau = int(X), int(Y)

    PX = X
    PY = Y
    Temps_debut = temps_maintenant

    return


def rester_a_ecran():

    global marge_ecran, position_vaisseau, dimensions_fenetre

    ecranX = dimensions_fenetre[0]
    ecranY = dimensions_fenetre[1]

    X = position_vaisseau[0]
    Y = position_vaisseau[1]

    if X < -marge_ecran :
        X = ecranX + marge_ecran
    elif X > ecranX + marge_ecran:
        X = - marge_ecran
    elif Y < -marge_ecran:
        Y = ecranY + marge_ecran
    elif Y > ecranY + marge_ecran:
        Y = - marge_ecran

    position_vaisseau = X, Y


# Initialisation


pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 7")

horloge = pygame.time.Clock()
couleur_fond = NOIR

pygame.key.set_repeat(10, 10)

initialiser_calculs()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            gerer_touche(evenement.key)

    fenetre.fill(couleur_fond)

    mettre_a_jour_position()
    rester_a_ecran()

    afficher_vaisseau(position_vaisseau, orientation)

    pygame.display.flip()

    if compteur_propulseur != 0:
        compteur_propulseur -= 1
        if compteur_propulseur == 0:
            force_poussee = 0

    horloge.tick(images_par_seconde)