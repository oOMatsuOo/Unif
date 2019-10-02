# ------------------------------------------------------------------------
# Laboratoires de programmation mathÃ©matique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 1: Conversion entre le systÃ¨mes de coordonnÃ©es du terrain
#              et celui de la fenÃªtre.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        dist_terrain_vers_fenetre(),
#                        coord_terrain_vers_fenetre(),
#                        dist_fenetre_vers_terrain(),
#                        coord_fenetre_vers_terrain(),
#                        temps_tics_vers_secondes()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLANC = (255, 255, 255)
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)

### Fonctions

# *** A MODIFIER *********************************************************

def dist_terrain_vers_fenetre(dist_t, largeur_fenetre, largeur_terrain):
    
    dist_f = (largeur_fenetre/ largeur_terrain) * dist_t

    return dist_f

# *** A MODIFIER *********************************************************

def coord_terrain_vers_fenetre(point_terrain, dimensions_fenetre,
                               largeur_terrain):
    x_t, y_t = point_terrain
    longeur_fenetre, largeur_fenetre = dimensions_fenetre

    longeur_terrain = longeur_fenetre * (largeur_terrain/largeur_fenetre)
    
    x_f = dist_terrain_vers_fenetre(x_t, longeur_fenetre, longeur_terrain) + longeur_fenetre/2
    y_f = -dist_terrain_vers_fenetre(y_t, largeur_fenetre, largeur_terrain) + largeur_fenetre/2
    
    return (x_f, y_f)

# *** A MODIFIER *********************************************************

def dist_fenetre_vers_terrain(dist_f, largeur_fenetre, largeur_terrain):

    dist_t = dist_f * (largeur_terrain/largeur_fenetre) 
    
    return dist_t

# *** A MODIFIER *********************************************************

def coord_fenetre_vers_terrain(point_fenetre, dimensions_fenetre,
                               largeur_terrain):
    x_f, y_f = point_fenetre
    longeur_fenetre, largeur_fenetre = dimensions_fenetre
    longeur_terrain = longeur_fenetre * (largeur_terrain/largeur_fenetre)

    x_t = x_f * (longeur_terrain / longeur_fenetre)  - longeur_terrain/2
    y_t = -y_f * (largeur_terrain / largeur_fenetre) +  largeur_terrain/2
    
    return (x_t, y_t)

# *** A MODIFIER *********************************************************

def temps_tics_vers_secondes(t_t, tics_par_seconde):

    t_s = t_t/tics_par_seconde
    return t_s

# ************************************************************************

# Affichage d'un disque sur le terrain

def dessiner_disque(x, y, r, couleur, fenetre, dimensions_fenetre,
                    largeur_terrain):
    x_f, y_f = coord_terrain_vers_fenetre((x, y),
                                          dimensions_fenetre,
                                          largeur_terrain)
    r_f = dist_terrain_vers_fenetre(r, dimensions_fenetre[0], largeur_terrain)
    pygame.draw.circle(fenetre, couleur, (int(x_f), int(y_f)), int(r_f))
    return

# Affichage d'un texte sur le terrain

def afficher_texte(texte, position, dimensions, couleur_texte, couleur_fond,
                   fenetre, dimensions_fenetre, largeur_terrain):
    x_f, y_f = coord_terrain_vers_fenetre(position,
                                          dimensions_fenetre,
                                          largeur_terrain)
    largeur_f = dist_terrain_vers_fenetre(dimensions[0], dimensions_fenetre[0],
                                          largeur_terrain)
    hauteur_f = dist_terrain_vers_fenetre(dimensions[1], dimensions_fenetre[0],
                                          largeur_terrain)

    image = police.render(texte, True, couleur_texte)
    panneau = pygame.Surface((largeur_f, hauteur_f))
    panneau.fill(couleur_fond)
    panneau.blit(image, (0, 0))
    fenetre.blit(panneau, (x_f, y_f))
  
### ParamÃ¨tre(s)

dimensions_fenetre = (800, 600)  # en pixels
dimensions_terrain = (4.0, 3.0)  # en mÃ¨tres
taille_texte = 16                # en pixels
images_par_seconde = 50

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 1");

horloge = pygame.time.Clock()
police  = pygame.font.SysFont("monospace", taille_texte)
couleur_fond = NOIR

# Dessin

fenetre.fill(couleur_fond)
dessiner_disque(0.0,  0.0, 1.00, JAUNE, fenetre, dimensions_fenetre,
                dimensions_terrain[0])
dessiner_disque(-0.4,  0.1, 0.15, NOIR,  fenetre, dimensions_fenetre,
                dimensions_terrain[0])
dessiner_disque(0.4,  0.1, 0.10, NOIR,  fenetre, dimensions_fenetre,
                dimensions_terrain[0])

for i in range(30):
    alpha = (i - 15) / 25.0;
    x = math.sin(alpha) * 0.3
    y = -0.1 - math.cos(alpha) * 0.3
    dessiner_disque(x, y, 0.10, ROUGE, fenetre, dimensions_fenetre,
                    dimensions_terrain[0])

# Boucle principale

temps = 0.0
temps_clic = -1000.0


while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif (evenement.type == pygame.MOUSEBUTTONDOWN
              and evenement.button == 1):
            x_t, y_t = coord_fenetre_vers_terrain(evenement.pos,
                                                  dimensions_fenetre,
                                                  dimensions_terrain[0])
            afficher_texte("({0:.2f}m, {1:.2f}m)".format(x_t, y_t),
                           (-1.9, -1.3), (1.0, 0.1),
                           BLANC, couleur_fond, fenetre, dimensions_fenetre,
                           dimensions_terrain[0])

            temps_dernier_clic = temps_clic
            temps_clic = temps_tics_vers_secondes(temps, images_par_seconde)
            delai_clic = temps_clic - temps_dernier_clic
      
            if delai_clic < 1.0:
                texte = "{0:.2f}s".format(delai_clic)
            else:
                texte = "Lent"
      
            afficher_texte(texte, (1.6, -1.3), (0.3, 0.1),
                           BLANC, NOIR, fenetre, dimensions_fenetre,
                           dimensions_terrain[0])

    pygame.display.flip()
    horloge.tick(images_par_seconde)
    temps += 1
