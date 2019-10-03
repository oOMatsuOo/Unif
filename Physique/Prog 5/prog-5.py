# ------------------------------------------------------------------------
# Laboratoires de programmation mathematique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 5: Vecteurs vitesse et acceleration, detection de gestes.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        deplacer_pol(),
#                        dessiner_vecteur(),
#                        initialiser_calculs(),
#                        calculer_vitesse_acceleration_2d() et
#                        detecter_geste()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLEU = (0, 0, 255)
JAUNEMIEL = (255, 192, 0)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

A = 2
B = 5
C = 20

### Fonctions

# *** A MODIFIER *********************************************************

def deplacer_pol(point, distance, orientation):

    X, Y = point
    
    a = math.cos(orientation)*distance
    b = math.sin(orientation)*distance

    Xr = X + a
    Yr = Y + b 

    return (Xr, Yr)

# *** A MODIFIER *********************************************************

def dessiner_vecteur(fenetre, couleur, origine, vecteur):

    pi = math.pi
    Xv, Yv = vecteur
    distance = math.sqrt(math.pow(Xv,2)+math.pow(Yv,2))
    orientation = math.atan2(Yv, Xv)
    p = origine
    Xp, Yp = p 

    if distance >= C:
        p4 = (Xp+Xv,Yp+Yv)
        p1 = deplacer_pol(p, A, orientation+(pi/2))
        p7 = deplacer_pol(p, A, orientation-(pi/2))

        Xp4, Yp4 = p4
        distancepp4 = math.sqrt(math.pow((Xp4-Xp),2)+ math.pow((Yp4-Yp),2))-C

        p2 = deplacer_pol(p1, distancepp4, orientation)
        p6 = deplacer_pol(p7, distancepp4, orientation)
        p3 = deplacer_pol(p2, B, orientation-(pi/2))
        p5 = deplacer_pol(p6, B, orientation+(pi/2))

        polygone = [p1,p2,p3,p4,p5,p6,p7]
        pygame.draw.polygon(fenetre, couleur, polygone)
    else:
        p3 = (Xp+Xv,Yp+Yv)
        p1 = deplacer_pol(p3,C,(orientation+pi))
        p2 = deplacer_pol(p1, (A+B), (orientation-(pi/2)))
        p4 = deplacer_pol(p1, (A+B), (orientation+(pi/2)))

        polygone2 = [p2,p3,p4]
        pygame.draw.polygon(fenetre, couleur, polygone2)

    return

# *** A MODIFIER *********************************************************

def initialiser_calculs():

    global Position_X
    global Position_Y
    global Temps_debut
    global Vitesse_X
    global Vitesse_Y

    Position_X = 0
    Position_Y = 0
    Temps_debut = 0
    Vitesse_X = 0
    Vitesse_Y = 0

    return

# *** A MODIFIER *********************************************************

def calculer_vitesse_acceleration_2d(position, temps_maintenant):

    global Position_X
    global Position_Y
    global Temps_debut
    global Vitesse_X
    global Vitesse_Y

    X, Y = position

    Vx = -(Position_X - X)/ (temps_maintenant - Temps_debut)
    Vy = -(Position_Y - Y)/ (temps_maintenant - Temps_debut)
    Ax = (Vx - Vitesse_X) / (temps_maintenant - Temps_debut)
    Ay = (Vy - Vitesse_Y) / (temps_maintenant - Temps_debut)

    Position_X = X
    Position_Y = Y
    Temps_debut = temps_maintenant
    Vitesse_X = Vx
    Vitesse_Y = Vy

    return (Vx, Vy), (Ax, Ay)

# *** A MODIFIER *********************************************************

def detecter_geste(vitesse, acceleration):

    vx , vy = vitesse
    ax , ay = acceleration

    orientation = math.atan2(vy, vx)
    pi = math.pi
    marge_erreur = math.radians(10)
    detect_gest = False

    longueur_v = math.sqrt(math.pow(vx,2) + math.pow(vy,2))
    longueur_a = math.sqrt(math.pow(ax,2) + math.pow(ay,2))

    if(longueur_v < 0.2 and longueur_a > 0.002):
        if( orientation < ((pi/2)+marge_erreur) and orientation > ((pi/2)-marge_erreur)):
            detect_gest = True
    else:
        detect_gest = False

    return (detect_gest)

# ************************************************************************

def afficher_compteur():
    image = police.render(str(compteur), True, NOIR) 
    fenetre.blit(image, (50, 50))
    return

def amortir(v, ancien_v, coefficient):
    return (ancien_v[0] * coefficient + v[0] * (1.0 - coefficient),
            ancien_v[1] * coefficient + v[1] * (1.0 - coefficient))

def traiter_mouvement(position):
    global premier_mouvement, ancienne_position, ancienne_acceleration
    global compteur, derniere_detection

    if premier_mouvement:
        premier_mouvement = False
    else:
        x, y = position
        
        # Amortissement pour lisser les mouvements.
        position = amortir(position, ancienne_position,
                           amortissement_position)

        t = pygame.time.get_ticks()
        v, a = calculer_vitesse_acceleration_2d(position, t)

        a = amortir(a, ancienne_acceleration, amortissement_acceleration)
        ancienne_acceleration = a

        if detecter_geste(v, a) and t > derniere_detection + 500:
            compteur += 1
            derniere_detection = t
            
        fenetre.fill(couleur_fond)

        afficher_compteur()
        
        pygame.draw.circle(fenetre, BLEU,
                           (int(position[0]), int(position[1])), 20)

        if doit_afficher_vitesse:
            dessiner_vecteur(fenetre, ROUGE, position,
                             (int(v[0] * facteur_vitesse),
                              int(v[1] * facteur_vitesse)))

        if doit_afficher_acceleration:
            dessiner_vecteur(fenetre, VERT, position,
                             (int(a[0] * facteur_acceleration),
                              int(a[1] * facteur_acceleration)))
            
        pygame.display.flip()

    ancienne_position = position        
    return

### Parametre(s)

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

couleur_fond = JAUNEMIEL

amortissement_position = 0.7
amortissement_acceleration = 0.5
facteur_vitesse = 200
facteur_acceleration = 40000

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 5");

horloge = pygame.time.Clock()
police  = pygame.font.SysFont("monospace", 36)

premier_mouvement = True

ancienne_acceleration = (0.0, 0.0)

doit_afficher_vitesse = True
doit_afficher_acceleration = True

compteur = 0

derniere_detection = -1000

fenetre.fill(couleur_fond)
pygame.display.flip()

# Boucle principale

initialiser_calculs()

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_a:
                doit_afficher_acceleration = not doit_afficher_acceleration
            elif evenement.key == pygame.K_v:
                doit_afficher_vitesse = not doit_afficher_vitesse

    traiter_mouvement(pygame.mouse.get_pos())        
    horloge.tick(images_par_seconde)