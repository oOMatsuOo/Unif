# ------------------------------------------------------------------------
# Laboratoires de programmation mathÃ©matique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 2: Jeu de tir.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        mru_1d() et
#                        calculer_tir()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLANC = (255, 255, 255)
BLEUCLAIR = (127, 127, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

### Fonctions

# *** A MODIFIER *********************************************************

def mru_1d(depart, temps_depart, vitesse, temps_maintenant):
    
    p = depart + (temps_maintenant - temps_depart)*vitesse
    
    return p

# *** A MODIFIER *********************************************************

def calculer_tir(depart, cible, vitesse, prochain_temps_cible,
                 temps_maintenant):
    temps_tir = 0
    distance = cible - depart
    temps_trajet = distance / vitesse
    temps_restant = prochain_temps_cible - temps_maintenant

    if temps_trajet <= temps_restant:
        tir_est_possible = True
    else:
        tir_est_possible = False

    if tir_est_possible:
        temps_tir = prochain_temps_cible - temps_trajet
    
    return (tir_est_possible, temps_tir)

# ************************************************************************

def dessiner_canon(position, fenetre):
    if tir_est_arme:
        pygame.draw.circle(fenetre, ROUGE, list(map(int, position)), 20)
    else:
        pygame.draw.circle(fenetre, BLEUCLAIR, list(map(int, position)), 20)
    return

def dessiner_cible(position, fenetre):
    pygame.draw.circle(fenetre, NOIR, list(map(int, position)), 10)
    return

def dessiner_balles(balles, fenetre):
    for balle in balles:
        position = (balle['position_depart'][0],
                    mru_1d(balle['position_depart'][1],
                           balle['temps_depart'],
                           balle['vitesse_verticale'],
                           pygame.time.get_ticks()))
        
        pygame.draw.circle(fenetre, BLANC, list(map(int, position)), 5)
    return

def ajouter_balle(balles, position, temps_depart, vitesse):
    balles.append({'position_depart': position,
                   'temps_depart': temps_depart,
                   'vitesse_verticale': vitesse})
    return

def balle_dans_cible(balle, position_cible, temps_maintenant):
    position_balle = (balle['position_depart'][0],
                      mru_1d(balle['position_depart'][1],
                             balle['temps_depart'],
                             balle['vitesse_verticale'],
                             temps_maintenant))

    return (abs(position_balle[0] - position_cible[0]) < 10
            and abs(position_balle[1] - position_cible[1]) < 10)
  
def tri_balles(balles, position_cible):
    temps_maintenant = pygame.time.get_ticks()
    ballesTriees = []
    points = 0
  
    for balle in balles:
        if temps_maintenant - balle['temps_depart'] > 4000:
            continue

        if balle_dans_cible(balle, position_cible, temps_maintenant):
            points += 1
        else:
            ballesTriees.append(balle)
 
    return (ballesTriees, points)

def afficher_score(score, fenetre):
    image = police.render(str(score), True, ROUGE)
    panneau = pygame.Surface((150, 36))
    panneau.fill(VERT)
    panneau.blit(image, (0, 0))
    fenetre.blit(panneau, (50, 50))
    return

def armer_tir_automatique(temps_tir, vitesse_balle):
    global tir_est_arme, temps_tir_automatique, vitesse_tir_automatique

    if not tir_est_arme:
        tir_est_arme = True
        temps_tir_automatique = temps_tir
        vitesse_tir_automatique = vitesse_balle

    return

def essayer_tir_automatique(vitesse_balle):

    prochain_temps_cible = ((temps_maintenant // demi_periode_cible + 1)
                            * demi_periode_cible)

    tirPossible, temps_tir = calculer_tir(position_canon[1],
                                          position_cible[1],
                                          -vitesse_balle,
                                          prochain_temps_cible,
                                          temps_maintenant)

    if tirPossible:
        armer_tir_automatique(temps_tir, vitesse_balle)
  
    return

def gerer_bouton(bouton):
    if bouton == 1:
        ajouter_balle(balles, position_canon, temps_maintenant,
                       -vitesse_balles)
    elif bouton == 3:
      ajouter_balle(balles, position_canon, temps_maintenant,
                    -vitesse_balles * 2)
    return

def gerer_touche(touche):
    if touche == pygame.K_l:
        essayer_tir_automatique(vitesse_balles)
    elif touche == pygame.K_r:
        essayer_tir_automatique(vitesse_balles * 2)
    return
    
### ParamÃ¨tre(s)

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25
vitesse_balles = 0.2             # en pixels/milliseconde, multipliÃ©e
                                 # par 2 pour les balles rapides

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 2");

horloge = pygame.time.Clock()
police  = pygame.font.SysFont("monospace", 36)

couleur_fond = VERT
position_canon = (dimensions_fenetre[0] / 2, dimensions_fenetre[1] * 5 / 6)
position_cible = [ position_canon[0], dimensions_fenetre[1] / 6 ]

demi_periode_cible = 2500
amplitude_cible = 100

balles = []
score  = 0
tir_est_arme = False
temps_tir_automatique = 0
vitesse_tir_automatique = 0.0

# Boucle principale

while True:
    temps_maintenant = pygame.time.get_ticks()
  
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton(evenement.button)
        elif evenement.type == pygame.KEYDOWN:
            gerer_touche(evenement.key)

    fenetre.fill(couleur_fond)
    dessiner_canon(position_canon, fenetre)

    position_cible[0] = (position_canon[0] + amplitude_cible
                         * math.sin(float(temps_maintenant) /
                                    demi_periode_cible * math.pi))
    dessiner_cible(position_cible, fenetre)

    if tir_est_arme and temps_tir_automatique <= temps_maintenant:
        ajouter_balle(balles, position_canon,
                      temps_maintenant, -vitesse_tir_automatique)
        tir_est_arme = False
    
    dessiner_balles(balles, fenetre)
    balles, points = tri_balles(balles, position_cible)

    score += points
    afficher_score(score, fenetre)
  
    pygame.display.flip()
    horloge.tick(images_par_seconde)
