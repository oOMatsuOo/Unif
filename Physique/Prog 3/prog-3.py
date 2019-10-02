 # ------------------------------------------------------------------------
# Laboratoires de programmation mathématique et physique 1                
# ------------------------------------------------------------------------
# 
# Programme 3: Avion.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        initialiser_calculs(),
#                        calculer_vitesse_acceleration(),
#                        mrua_1d() et
#                        calculer_tir()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

BLEUCIEL = (127, 255, 255)
NOIR = (0, 0, 0)
ORANGE = (255, 127, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

GRAVITE = 0.0002  # en pixels/(ms)^2

### Fonctions

# *** A MODIFIER *********************************************************

def initialiser_calculs():
    global Position_0
    global Temps_debut
    global Vitesse_0

    Position_0 = altitude_avion
    Temps_debut = 0
    Vitesse_0 = 0

    return 
# *** A MODIFIER *********************************************************

def calculer_vitesse_acceleration(altitude_avion, temps_maintenant):
    global Position_0
    global Temps_debut
    global Vitesse_0

    Vy = (Position_0 - altitude_avion)/ (temps_maintenant - Temps_debut)
    Ay = (Vy - Vitesse_0) / (temps_maintenant - Temps_debut)

    Position_0 = altitude_avion
    Temps_debut = temps_maintenant
    Vitesse_0 = Vy

    return Vy, Ay

# *** A MODIFIER *********************************************************

def mrua_1d(depart, temps_depart, acceleration, temps_maintenant):

    temps_deplacement = temps_maintenant - temps_depart
    Vitesse = temps_deplacement * acceleration

    P = (temps_deplacement* Vitesse)/2 + depart 
    
    return P

# *** A MODIFIER *********************************************************

def calculer_tir(altitude_larguage, altitude_cible, acceleration,
                 prochain_temps_cible, temps_maintenant):

    Distance = altitude_cible - altitude_larguage
    temps_deplacement = math.sqrt(2*Distance/acceleration )
    temps_restant = prochain_temps_cible - temps_maintenant
    temps_tir = prochain_temps_cible - temps_deplacement
  
    if temps_deplacement <= temps_restant:
        tir_est_possible = True
    else:
        tir_est_possible = False

    return (tir_est_possible, temps_tir)

# ************************************************************************

def dessiner_sol(temps_maintenant):
    for x in range(dimensions_fenetre[0]):    
        alpha = ((-x - temps_maintenant * vitesse_horizontale)
                 * 2.0 * math.pi / periode_arriere_plan)
        y = hauteur_sol * math.exp(math.cos(alpha)) / math.e
        pygame.draw.rect(fenetre, VERT, ((x, dimensions_fenetre[1] - y),
                                         (1, y)))
    return
        
def dessiner_nuages(nuages, temps_maintenant):
    largeur_nuage = image_nuage.get_width()
    for nuage in nuages:
        x = (int(nuage[0] - temps_maintenant * vitesse_horizontale)
             % periode_arriere_plan - largeur_nuage)
        y = nuage[1]
        fenetre.blit(image_nuage, (x, y))
    return

def dessiner_avion(altitude):
    x = (dimensions_fenetre[0] - image_avion.get_width()) // 2
    y = int(altitude) - image_avion.get_height() // 2
    fenetre.blit(image_avion, (x, y))
    return

def dessiner_drapeau(temps_maintenant):
    x = int(-temps_maintenant * vitesse_horizontale) % periode_arriere_plan
    pygame.draw.polygon(fenetre, ROUGE, ((x, dimensions_fenetre[1] - 45),
                                         (x, dimensions_fenetre[1] - 25),
                                         (x + 20, dimensions_fenetre[1] - 35)))
    pygame.draw.rect(fenetre, NOIR, ((x, dimensions_fenetre[1] - 50), (3, 40)))
       
    return

def ajuster_altitude_avion(y):
    global altitude_avion

    position_max = dimensions_fenetre[1] - 50 - image_avion.get_height() // 2
    
    if y > position_max:
        y = position_max

    # amortissement pour lisser les mouvements
    
    altitude_avion = (altitude_avion * 5.0 + y) / 6.0
    return
    
def afficher_texte(x, y, texte, couleur):
    image = police.render(texte, True, couleur)
    fenetre.blit(image, (x, y))
    return

def variometre(x, y, v):
    global valeur_variometre

    # amortissement pour lisser l'affichage
    
    valeur_variometre = 0.8 * valeur_variometre + 0.2 * v
    
    H = 100
    L = 40
    E = 2
    
    indicateur = int((valeur_variometre + 1.0) * H / 2.0)

    if indicateur < E:
        indicateur = E
    elif indicateur >= H - E:
        indicateur = H - E

    afficher_texte(x + 10, y - 20, "Vy", NOIR)
    afficher_texte(x - 20, y + (H - taille_texte) // 2, "0-", NOIR)
        
    pygame.draw.rect(fenetre, NOIR, ((x, y), (L, H)))
    pygame.draw.rect(fenetre, VERT, ((x, y + H - indicateur - E), (L, 2 * E)))
    
    return

def accelerometre(x, y, v):
    global valeur_accelerometre

    # amortissement pour lisser l'affichage

    GAIN = 200
    
    valeur_accelerometre = 0.8 * valeur_accelerometre + 0.2 * v * GAIN
    
    H = 100
    L = 40
    E = 2
    
    indicateur = int((valeur_accelerometre + 1.0) * H / 2.0)

    if indicateur < E:
        indicateur = E
    elif indicateur >= H - E:
        indicateur = H - E

    afficher_texte(x + 10, y - 20, "Ay", NOIR)
    afficher_texte(x - 20, y + (H - taille_texte) // 2, "0-", NOIR)
        
    pygame.draw.rect(fenetre, NOIR, ((x, y), (L, H)))
    pygame.draw.rect(fenetre, ROUGE, ((x, y + H - indicateur - E), (L, 2 * E)))
    
    return

def dessiner_bombes(bombes):
    temps_maintenant = pygame.time.get_ticks()
    for bombe in bombes:
        position = (bombe['position_depart'][0],
                    mrua_1d(bombe['position_depart'][1],
                            bombe['temps_depart'],
                            bombe['acceleration_verticale'],
                            temps_maintenant))
        pygame.draw.circle(fenetre, ORANGE, list(map(int, position)), 10)
    return    

def ajouter_bombe(bombes, position, temps_depart, acceleration):
    bombes.append({'position_depart': position,
                   'temps_depart': temps_depart,
                   'acceleration_verticale': acceleration})
    return

def tri_bombes(bombes):
    temps_maintenant = pygame.time.get_ticks()
    return list(filter(lambda x: x['temps_depart']
                        > temps_maintenant - 3000, bombes))

def armer_tir_automatique(temps_tir):
    global tir_est_arme, temps_tir_automatique

    if not tir_est_arme:
        tir_est_arme = True
        temps_tir_automatique = temps_tir

    return

def essayer_tir_automatique():
    periode = periode_arriere_plan / vitesse_horizontale
    prochain_temps_cible = -dimensions_fenetre[0] / (2.0 * vitesse_horizontale)

    while prochain_temps_cible < temps_maintenant:
        prochain_temps_cible += periode

    tirPossible, temps_tir = calculer_tir((altitude_avion
                                           + offset_larguage_bombe),
                                          dimensions_fenetre[1],
                                          GRAVITE,
                                          prochain_temps_cible,
                                          temps_maintenant)
    if tirPossible:
        armer_tir_automatique(temps_tir)
    
    return

def gerer_touche(touche):
    if touche == pygame.K_b:
        ajouter_bombe(bombes, (dimensions_fenetre[0] // 2,
                               altitude_avion + offset_larguage_bombe),
                          temps_maintenant, GRAVITE)
    elif touche == pygame.K_a:
        essayer_tir_automatique()
    return

### Paramètre(s)

dimensions_fenetre = (800, 600)  # en pixels
taille_texte = 16  
images_par_seconde = 25
vitesse_horizontale = 0.125  # en pixels par milliseconde
hauteur_sol = 20

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 3");

horloge = pygame.time.Clock()
police  = pygame.font.SysFont("monospace", taille_texte)
couleur_fond = BLEUCIEL

nuages = [(0, 100), (600, 300), (200, 350)]
image_nuage = pygame.image.load('images/cloud.png').convert_alpha(fenetre)

altitude_avion = dimensions_fenetre[1] / 2
image_avion = pygame.image.load('images/plane.png').convert_alpha(fenetre)
offset_larguage_bombe = image_avion.get_height() // 2 - 10

periode_arriere_plan = dimensions_fenetre[0] + image_nuage.get_width()

valeur_variometre = 0.0
valeur_accelerometre = 0.0

bombes = []
tir_est_arme = False
temps_tri_automatique = 0

# Boucle principale

initialiser_calculs()

while True:
    temps_maintenant = pygame.time.get_ticks()
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.MOUSEMOTION:
            ajuster_altitude_avion(evenement.pos[1])
        elif evenement.type == pygame.KEYDOWN:
            gerer_touche(evenement.key)

    vitesse_v, acceleration_v = calculer_vitesse_acceleration(altitude_avion,
                                                              temps_maintenant)

    if tir_est_arme and temps_tir_automatique <= temps_maintenant:
        ajouter_bombe(bombes, (dimensions_fenetre[0] // 2,
                               altitude_avion + offset_larguage_bombe),
                      temps_maintenant, GRAVITE)
        tir_est_arme = False

    fenetre.fill(couleur_fond)
    dessiner_nuages(nuages, temps_maintenant)
    dessiner_bombes(bombes)
    dessiner_sol(temps_maintenant)
    dessiner_drapeau(temps_maintenant)
    dessiner_avion(altitude_avion)

    variometre(dimensions_fenetre[0] // 20, dimensions_fenetre[1] // 10,
               vitesse_v)
    
    accelerometre(dimensions_fenetre[0] * 3 // 20, dimensions_fenetre[1] // 10,
                  acceleration_v)

    if tir_est_arme:
        afficher_texte(dimensions_fenetre[0] // 20,
                       3 * dimensions_fenetre[1] // 10,
                       "tir armé", NOIR)

    bombes = tri_bombes(bombes)

    pygame.display.flip()
    horloge.tick(images_par_seconde)
 
