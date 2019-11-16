#Beaujean Antoine
#Van Muysewinkel Kieran

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

dimensions_fenetre = (1000, 800)  # en pixels
images_par_seconde = 25

position_vaisseau = ([400, 300])
rayon_vaisseau = 15
orientation = 0

compteur_propulseur = 0

masse = 1
force_poussee = 0

k = 0.001

marge_ecran = 50

position_planete = ([325, 350])

planete_presente = 0

rayon_planete = 20
masse_planete = 1600

energie_cinetique = 0
energie_potentielle = 0

QUITTER = 0


# Fonctions

def afficher_vaisseau():
    pi = math.pi

    global compteur_propulseur, rayon_vaisseau

    p = (int(position_vaisseau[0]),int(position_vaisseau[1]))
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


def calcul_collision():
    global rayon_vaisseau, QUITTER

    position_VX = position_vaisseau[0]
    position_VY = position_vaisseau[1]

    position_PX = position_planete[0]
    position_PY = position_planete[1]
 
    vaisseau_rect = pygame.Rect((position_VX - rayon_vaisseau, position_VY - rayon_vaisseau), (rayon_vaisseau*2, rayon_vaisseau*2))
    planete_rect = pygame.Rect((position_PX - rayon_planete, position_PY - rayon_planete), (rayon_planete*2, rayon_planete*2))

    if planete_presente:
        if vaisseau_rect.colliderect(planete_rect):
            QUITTER = 1


def initialiser_calculs():

    global Temps_debut, VX, VY, PX, PY, position_vaisseau

    Temps_debut = 0
    PX = float(position_vaisseau[0])
    PY = float(position_vaisseau[1])
    VX = float(0)
    VY = float(0)

    return


def mettre_a_jour_position(temps):

    global Temps_debut, VX, VY, PX, PY, position_vaisseau, masse, force_poussee, orientation, masse_planete, position_planete, energie_cinetique, energie_potentielle

    temps_maintenant = pygame.time.get_ticks()

    delta_temps = temps - Temps_debut

    X = position_vaisseau[0]
    Y = position_vaisseau[1]

    XP = position_planete[0]
    YP = position_planete[1]

    delta_X = XP - X
    delta_Y = YP - Y

    distance = math.sqrt(delta_X**2 + delta_Y**2)

    if planete_presente:
        asin_orientationP = math.asin(delta_Y/ distance)
        acos_orientationP = math.acos(delta_X / distance)

        Force_attraction = (k * (masse_planete * masse) / distance**2 )

        ax = ((math.cos(orientation) * force_poussee) + (math.cos(acos_orientationP) * Force_attraction)) / masse
        ay = ((math.sin(orientation) * force_poussee) + (math.sin(asin_orientationP) * Force_attraction)) / masse

        energie_potentielle = -k * masse * masse_planete / distance 

    else:
        a = force_poussee / masse
        ax = math.cos(orientation) * a
        ay = math.sin(orientation) * a

        energie_potentielle = 0

    VX += ax * delta_temps
    VY += ay * delta_temps

    X = VX * delta_temps + X
    Y = VY * delta_temps + Y

    position_vaisseau = X, Y

    PX = X
    PY = Y
    Temps_debut = t

    energie_cinetique = masse * (VX**2+VY**2) / 2

    return

def afficher_tableau_de_bord():

    energie_cinetique_texte   = "Energie cinétique    : {0:.2f}".format(energie_cinetique * 1000)
    energie_potentielle_texte = "Energie potentielle  : {0:.2f}".format(energie_potentielle * 1000)
    somme                     = "Somme des énergies   : {0:.2f}".format((energie_potentielle + energie_cinetique) * 1000)

    police = pygame.font.SysFont("monospace", 16)

    image_energie_cinetique = police.render(energie_cinetique_texte, True, VIOLET)
    fenetre.blit(image_energie_cinetique,(dimensions_fenetre[0]//10,dimensions_fenetre[1]//10 - 40))

    image_energie_potentielle = police.render(energie_potentielle_texte, True, VIOLET)
    image_somme = police.render(somme, True, VIOLET)



    if planete_presente :
        fenetre.blit(image_energie_potentielle,(dimensions_fenetre[0]//10,dimensions_fenetre[1]//10 - 20))
        fenetre.blit(image_somme,(dimensions_fenetre[0]//10,dimensions_fenetre[1]//10))


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
    
    global position_planete, planete_presente

    if touche == 3:
        planete_presente = 0
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
        force_poussee = 0.0003


# Initialisation


pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 7")

horloge = pygame.time.Clock()
couleur_fond = NOIR

pygame.key.set_repeat(10, 10)

initialiser_calculs()
temps_precedent = 0

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

    temps_maintenant = pygame.time.get_ticks()

    if QUITTER:
        pygame.quit()
        sys.exit()

    fenetre.fill(couleur_fond)

    for t in range(temps_precedent, temps_maintenant):
        mettre_a_jour_position(t)

    rester_a_ecran()

    afficher_planete()

    afficher_vaisseau()

    afficher_tableau_de_bord()

    pygame.display.flip()

    if compteur_propulseur != 0:
        compteur_propulseur -= 1
        if compteur_propulseur == 0:
            force_poussee = 0

    temps_precedent = temps_maintenant

    horloge.tick(images_par_seconde)