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

dimensions_fenetre = (1300, 700)  # en pixels
images_par_seconde = 25

position_vaisseau = ([650, 350])
rayon_vaisseau = 15
orientation = 0

compteur_propulseur = 0

masse = 1
force_poussee = 0

k = 0.01

marge_ecran = 50

position_planete = ([325, 350])
position_planete2 = ([975, 350])

planete_presente = 1
planete_presente2 = 1

rayon_planete = 40
masse_planete = 1600

QUITTER = 0


# Fonctions

def afficher_vaisseau():
    pi = math.pi

    global compteur_propulseur, rayon_vaisseau

    p = position_vaisseau
    r = 23
    a = orientation
    b = pi / 7

    if compteur_propulseur != 0:    # Affiche Flammes
        dessiner_triangle(ROUGE, p, 38, (a + pi + 21 * pi / 20), (pi / 30))
        dessiner_triangle(ROUGE, p, 38, (a + pi + 19 * pi / 20), (pi / 30))

    dessiner_triangle(ORANGE, p, r, a, b)   # Affiche orientation

    pygame.draw.circle(fenetre, GRIS, p, rayon_vaisseau)  # Affiche vaisseau


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


def afficher_planete():
    global position_planete, planete_presente, rayon_planete

    if planete_presente:
        pygame.draw.circle(fenetre, ROUGE, position_planete, rayon_planete)


def afficher_planete2():
    global position_planete2, planete_presente2, rayon_planete

    if planete_presente2:
        pygame.draw.circle(fenetre, ORANGE, position_planete2, rayon_planete)


def calcul_collision():
    global rayon_vaisseau, QUITTER

    position_VX = position_vaisseau[0]
    position_VY = position_vaisseau[1]

    position_PX = position_planete[0]
    position_PY = position_planete[1]

    PX2 = position_planete2[0]
    PY2 = position_planete2[1]
 
    vaisseau_rect = pygame.Rect((position_VX - rayon_vaisseau, position_VY - rayon_vaisseau), (rayon_vaisseau*2, rayon_vaisseau*2))
    planete_rect = pygame.Rect((position_PX - rayon_planete, position_PY - rayon_planete), (rayon_planete*2, rayon_planete*2))
    planete_rect2 = pygame.Rect((PX2 - rayon_planete, PY2 - rayon_planete), (rayon_planete*2, rayon_planete*2))

    if planete_presente:
        if vaisseau_rect.colliderect(planete_rect):
            QUITTER = 1

    if planete_presente2:
        if vaisseau_rect.colliderect(planete_rect2):
            QUITTER = 1


def initialiser_calculs():

    global Temps_debut, VX, VY, PX, PY, position_vaisseau

    Temps_debut = 0
    PX = float(position_vaisseau[0])
    PY = float(position_vaisseau[1])
    VX = float(0)
    VY = float(0)

    return


def mettre_a_jour_position():

    global Temps_debut, VX, VY, PX, PY, position_vaisseau, masse, force_poussee, orientation, masse_planete, position_planete, position_planete2

    temps_maintenant = pygame.time.get_ticks()

    delta_temps = temps_maintenant - Temps_debut

    X = position_vaisseau[0]
    Y = position_vaisseau[1]

    XP = position_planete[0]
    YP = position_planete[1]

    XP2 = position_planete2[0]
    YP2 = position_planete2[1]

    delta_X = XP - X
    delta_Y = YP - Y

    delta_X2 = XP2 - X
    delta_Y2 = YP2 - Y

    distance = math.sqrt(delta_X**2 + delta_Y**2)
    distance2 = math.sqrt(delta_X2**2 + delta_Y2**2)

    if planete_presente and planete_presente2:
        asin_orientationP = math.asin(delta_Y/ distance)
        acos_orientationP = math.acos(delta_X / distance)

        asin_orientationP2 = math.asin(delta_Y2/distance2)
        acos_orientationP2 = math.acos(delta_X2/distance2)

        Force_attraction = (k * (masse_planete * masse) / distance**2 )
        Force_attraction2 = (k * (masse_planete * masse) / distance2**2)

        ax = ((math.cos(orientation) * force_poussee) + (math.cos(acos_orientationP) * Force_attraction) + (math.cos(acos_orientationP2) * Force_attraction2)) / masse
        ay = ((math.sin(orientation) * force_poussee) + (math.sin(asin_orientationP) * Force_attraction) + (math.sin(asin_orientationP2) * Force_attraction2)) / masse
    
    elif planete_presente:
        asin_orientationP = math.asin(delta_Y/ distance)
        acos_orientationP = math.acos(delta_X / distance)

        Force_attraction = (k * (masse_planete * masse) / distance**2 )

        ax = ((math.cos(orientation) * force_poussee) + (math.cos(acos_orientationP) * Force_attraction)) / masse
        ay = ((math.sin(orientation) * force_poussee) + (math.sin(asin_orientationP) * Force_attraction)) / masse
    
    elif planete_presente2:
        asin_orientationP2 = math.asin(delta_Y2/ distance2)
        acos_orientationP2 = math.acos(delta_X2 / distance2)

        Force_attraction2 = (k * (masse_planete * masse) / distance2**2 )

        ax = ((math.cos(orientation) * force_poussee) + (math.cos(acos_orientationP2) * Force_attraction2)) / masse
        ay = ((math.sin(orientation) * force_poussee) + (math.sin(asin_orientationP2) * Force_attraction2)) / masse

    else:
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


def gerer_bouton(touche):
    
    global position_planete, planete_presente, position_planete2, planete_presente2

    if touche == 3:
        position_planete2 = evenement.pos
        planete_presente2 = 1
    elif touche == 1:
        position_planete = evenement.pos
        planete_presente = 1


def gerer_touche(touche):
    pi = math.pi
    global orientation, compteur_propulseur, force_poussee

    if touche == pygame.K_LEFT:
        orientation -= pi / 20
    elif touche == pygame.K_RIGHT:
        orientation += pi / 20
    elif touche == pygame.K_UP:
        compteur_propulseur += 3
        force_poussee = 0.001


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
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton(evenement.button)

    calcul_collision()

    if QUITTER:
        pygame.quit()
        sys.exit()

    fenetre.fill(couleur_fond)

    mettre_a_jour_position()

    #rester_a_ecran()

    afficher_planete()

    afficher_planete2()

    afficher_vaisseau()

    pygame.display.flip()

    if compteur_propulseur != 0:
        compteur_propulseur -= 1
        if compteur_propulseur == 0:
            force_poussee = 0

    horloge.tick(images_par_seconde)