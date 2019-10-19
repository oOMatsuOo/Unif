# ------------------------------------------------------------------------
# Laboratoires de programmation mathÃ©matique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 6: Tri balistique.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        mua_2d(),
#                        calculer_vitesse() et
#                        calculer_impact()  !!!
# 
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLEUCIEL = (127, 191, 255)
JAUNE = (255, 255, 0)
NOIR = (0, 0, 0)
ORANGE = (255, 192, 0)
ROUGE = (255, 0, 0)

### Fonctions

# *** A MODIFIER *********************************************************

def mua_2d(depart, temps_depart, vitesse_initiale, acceleration_verticale,
           temps_maintenant):

    V0x , V0y = vitesse_initiale
    X0, Y0 = depart
    a = acceleration_verticale
    
    temps_deplacement = temps_maintenant - temps_depart

    delta_x = V0x*temps_deplacement

    delta_y = V0y * temps_deplacement + a * temps_deplacement**2 /2

    X = X0 + delta_x
    Y = Y0 + delta_y

    return (X, Y)

# *** A MODIFIER *********************************************************

def calculer_vitesse(depart, angle, cible, acceleration_verticale):

    orientation = angle
    X0, Y0 = depart
    Cx, Cy = cible
    a = acceleration_verticale

    delta_x = Cx - X0
    delta_y = Cy - Y0

    V02 = (a*(delta_x**2)) / (2 * (math.cos(orientation)**2) * (delta_y - (math.tan(orientation) * delta_x)))

    V0 = 0
    if(V02 >= 0):
        tri_est_possible = True
        V0 = math.sqrt(V02)
    else:
        tri_est_possible = False

    return (tri_est_possible, V0)

# *** A MODIFIER *********************************************************

def calculer_impact(depart, angle, hauteur_sol, vitesse,
                    acceleration_verticale):
    X0, Y0 = depart
    V0 = vitesse
    g = acceleration_verticale
    Ys = hauteur_sol
    
    X1 = 0

    adt = g / 2
    bdt = V0 * math.sin(angle)
    cdt = Y0-Ys

    delta = bdt**2 - 4 * adt * cdt

    if delta > 0 :
        X1 = (-bdt + math.sqrt(delta)) / (2 * adt)

    Xs = V0  * math.cos(angle) * X1 + X0

    return (Xs)
    
# ************************************************************************

def dessiner_canon():
    p1 = (position_canon[0]
          + RAYON_CANON * math.cos(angle_canon + math.pi/2),
          position_canon[1]
          + RAYON_CANON * math.sin(angle_canon + math.pi/2))
    p4 = (position_canon[0]
          + RAYON_CANON * math.cos(angle_canon - math.pi/2),
          position_canon[1]
          + RAYON_CANON * math.sin(angle_canon - math.pi/2))
    pp = (LONGUEUR_CANON * math.cos(angle_canon),
          LONGUEUR_CANON * math.sin(angle_canon))
    p2 = (p1[0] + pp[0], p1[1] + pp[1])
    p3 = (p4[0] + pp[0], p4[1] + pp[1])
    pygame.draw.polygon(fenetre, ORANGE, [p1, p2, p3, p4])
    pygame.draw.circle(fenetre, JAUNE, position_canon,
                       RAYON_DISQUE_CANON)

    if vitesse_automatique:
        couleur_indicateur = ROUGE
    else:
        couleur_indicateur = ORANGE
        
    pygame.draw.rect(fenetre, couleur_fond,
                     ((position_canon[0] - LARGEUR_INDICATEUR // 2,
                       position_canon[1] + OFFSET_INDICATEUR),
                      (LARGEUR_INDICATEUR, HAUTEUR_INDICATEUR)))
    pygame.draw.rect(fenetre, couleur_indicateur,
                     ((position_canon[0] - LARGEUR_INDICATEUR // 2,
                       position_canon[1] + OFFSET_INDICATEUR),
                      (LARGEUR_INDICATEUR, HAUTEUR_INDICATEUR)), 4)

    if vitesse_tir > MAX_VITESSE:
        v = MAX_VITESSE
    elif vitesse_tir < MIN_VITESSE:
        v = MIN_VITESSE
    else:
        v = vitesse_tir
        
    y = int((v - MIN_VITESSE) * HAUTEUR_INDICATEUR
            / (MAX_VITESSE - MIN_VITESSE))

    pygame.draw.rect(fenetre, couleur_indicateur,
                     ((position_canon[0] - LARGEUR_INDICATEUR // 2,
                       position_canon[1] + OFFSET_INDICATEUR
                       + HAUTEUR_INDICATEUR - y),
                      (LARGEUR_INDICATEUR, y)))
    
    return

def ajouter_projectile():
    projectiles.append({'position_depart': position_canon,
                        'temps_depart': pygame.time.get_ticks(),
                        'vitesse_initiale':
                        (vitesse_tir * math.cos(angle_canon),
                         vitesse_tir * math.sin(angle_canon))})
    return

def dessiner_cible():
    if not cible_presente:
        return
    
    pygame.draw.circle(fenetre, ROUGE, position_cible, RAYON_CIBLE, 5)
    pygame.draw.rect(fenetre, ROUGE, ((position_cible[0] - 1,
                                       position_cible[1] - RAYON_CIBLE),
                                      (2, 2 * RAYON_CIBLE)))
    pygame.draw.rect(fenetre, ROUGE, ((position_cible[0] - RAYON_CIBLE,
                                       position_cible[1] - 1),
                                      (2 * RAYON_CIBLE, 2)))
    return
    
def dessiner_projectiles():
    temps_maintenant = pygame.time.get_ticks()
    for projectile in projectiles:
        position = mua_2d(projectile['position_depart'],
                          projectile['temps_depart'],
                          projectile['vitesse_initiale'],
                          GRAVITE,
                          temps_maintenant)
        pygame.draw.circle(fenetre, NOIR, list(map(int, position)), 8)
    return

def dessiner_impact():
    x = position_impact
    pygame.draw.polygon(fenetre, ROUGE, ((x, dimensions_fenetre[1] - 35),
                                         (x, dimensions_fenetre[1] - 15),
                                         (x + 20, dimensions_fenetre[1] - 25)))
    pygame.draw.rect(fenetre, NOIR, ((x, dimensions_fenetre[1] - 40), (3, 40)))
    return

def gerer_bouton(evenement):
    global position_cible, cible_presente, vitesse_automatique
    if evenement.button == 1:
        ajouter_projectile()
    elif evenement.button == 3:
        position_cible = evenement.pos
        cible_presente = True
        vitesse_automatique = False
    return    

def gerer_touche(touche):
    global angle_canon, vitesse_tir, cible_presente, vitesse_automatique
    global position_impact
    if touche == pygame.K_RIGHT:
        angle_canon += ANGLE_INCREMENT
        vitesse_automatique = False
        if angle_canon > MAX_ANGLE_CANON:
            angle_canon = MAX_ANGLE_CANON
    elif touche == pygame.K_LEFT:
        angle_canon -= ANGLE_INCREMENT
        vitesse_automatique = False
        if angle_canon < MIN_ANGLE_CANON:
            angle_canon = MIN_ANGLE_CANON
    elif touche == pygame.K_UP:
        if vitesse_tir < MIN_VITESSE:
            vitesse_tir = MIN_VITESSE
        vitesse_tir += VITESSE_INCREMENT
        vitesse_automatique = False
        if vitesse_tir > MAX_VITESSE:
           vitesse_tir = MAX_VITESSE
    elif touche == pygame.K_DOWN:
        if vitesse_tir > MAX_VITESSE:
            vitesse_tir = MAX_VITESSE
        vitesse_tir -= VITESSE_INCREMENT
        vitesse_automatique = False
        if vitesse_tir < MIN_VITESSE:
           vitesse_tir = MIN_VITESSE
    elif touche == pygame.K_a:
        if cible_presente:
            ok, v = calculer_vitesse(position_canon, angle_canon,
                                     position_cible, GRAVITE)
            if ok:
                vitesse_tir = v
                vitesse_automatique = True
                position_impact = calculer_impact(position_canon, angle_canon,
                                                  dimensions_fenetre[1], v,
                                                  GRAVITE)
                
    elif touche == pygame.K_c:
        cible_presente = False
    return

def tri_projectiles(projectiles):
    temps_maintenant = pygame.time.get_ticks()
    return list(filter(lambda x: x['temps_depart']
                        > temps_maintenant - 4000, projectiles))

### ParamÃ¨tre(s)

RAYON_DISQUE_CANON = 20
RAYON_CANON = 8
LONGUEUR_CANON = 35

LARGEUR_INDICATEUR = 25
HAUTEUR_INDICATEUR = 75
OFFSET_INDICATEUR = 50

MIN_VITESSE = 0.4
MAX_VITESSE = 1.5
VITESSE_INCREMENT = 0.05

RAYON_CIBLE = 15

ANGLE_INCREMENT = math.pi / 50
MAX_ANGLE_CANON = math.pi / 2 - 0.1
MIN_ANGLE_CANON = -math.pi / 2 + 0.1

GRAVITE = 0.001

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

couleur_fond = BLEUCIEL
position_canon = (50, 450)
angle_canon = -math.pi / 4

position_cible = (-100, -100)
cible_presente = False
vitesse_tir = 0.8
vitesse_automatique = False

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 6");

horloge = pygame.time.Clock()

pygame.key.set_repeat(10, 10)

projectiles = []

# Boucle principale

while True:
    temps_maintenant = pygame.time.get_ticks()
  
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton(evenement)
        elif evenement.type == pygame.KEYDOWN:
            gerer_touche(evenement.key)

    fenetre.fill(couleur_fond)

    if vitesse_automatique:
        dessiner_impact()
    
    dessiner_cible()
    dessiner_projectiles()
    dessiner_canon()

    projectiles = tri_projectiles(projectiles)
  
    pygame.display.flip()
    horloge.tick(images_par_seconde)