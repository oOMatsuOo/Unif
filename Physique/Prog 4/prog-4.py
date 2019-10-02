# ------------------------------------------------------------------------
# Laboratoires de programmation mathÃ©matique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 4: Affichage de vecteurs.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        deplacer_pol() et
#                        dessiner_vecteur()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

JAUNEMIEL = (255, 192, 0)
NOIR = (0, 0, 0)

A = 4
B = 10
C = 40

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
    
# ************************************************************************

def traiter_clic(position, bouton):
    global premier_clic, ancienne_position

    if bouton == 3:
        premier_clic = True
        fenetre.fill(couleur_fond)
        return

    if bouton != 1:
        return
    
    if premier_clic:
        premier_clic = False
    else:
        dessiner_vecteur(fenetre, NOIR, ancienne_position,
                         (position[0] - ancienne_position[0],
                          position[1] - ancienne_position[1]))
                         
    ancienne_position = position
    return

### ParamÃ¨tre(s)

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 4");

horloge = pygame.time.Clock()
couleur_fond = JAUNEMIEL

premier_clic = True

fenetre.fill(couleur_fond)

# Boucle principale

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            traiter_clic(evenement.pos, evenement.button)

    pygame.display.flip()
    horloge.tick(images_par_seconde)