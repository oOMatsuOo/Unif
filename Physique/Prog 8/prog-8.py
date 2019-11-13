import math
import pygame
import sys

# Constantes

JAUNEPALE = (255, 255, 192)
VIOLET    = (148,   0, 211)
ORANGE    = (255, 140,   0)

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
dimensions_fenetre_metre = (40, 30)
images_par_seconde = 120

a = 0.000165
b = 0
c = -0.055
d = 0
e = 5

vitesse = [0,0]
premiere_iteration = 0
temps_derniere_iteration = 0

µc = 0.03


# Conversion

def fenetre_vers_piste(position):
    Xf, Yf = position
    FL, FH = dimensions_fenetre
    FLM, FHM = dimensions_fenetre_metre

    Xp = ((Xf - (FL / 2)) / (FL / FLM))
    Yp = -((Yf - FH) / (FH / FHM))
    
    return(Xp, Yp)

def piste_vers_fenetre(position):
    Xp, Yp = position
    FL, FH = dimensions_fenetre
    FLM, FHM = dimensions_fenetre_metre

    Xf = ((Xp * (FL / FLM)) + (FL / 2))
    Yf = ((-Yp * (FH / FHM)) + FH)
    
    return(Xf, Yf)


# Fonction


def hauteur_piste(X):
    global a, c, e

    Y = a * X**4 + c * X**2 + e

    return(Y)


def derive_hauteur_piste(X):
    gamma = 1E-10

    alpha =  ( hauteur_piste(X + gamma) - hauteur_piste(X) ) / gamma 

    return(alpha)


# Dessin


def dessiner_piste():
    Xp = 0
    Yp = 0
    Xf = -1
    Yf = 0
    h = dimensions_fenetre[1]

    while(Xf <= dimensions_fenetre[0]):
        Xp = fenetre_vers_piste([Xf, 0])[0]
        Yp = hauteur_piste(Xp)
        Yf = piste_vers_fenetre([0, Yp])[1]
        Xf += 1
        point = [[Xf, Yf],[1, (h - Yf) + 1]]

        pygame.draw.rect(fenetre, VIOLET, point)

    return


def dessiner_mobile(position):
    Xp, Yp = position
    Xf, Yf = piste_vers_fenetre([Xp, Yp])

    pygame.draw.circle(fenetre, ORANGE, [int(Xf), int(Yf)], 10)
    
    return


def mettre_a_jour_position(position, temps):
    global vitesse, premiere_iteration, position_mobile, temps_precedent_position, Vl, norme_acceleration_ressentie
    Vx, Vy = vitesse
    X, Y = position
    t = temps_precedent_position / 1000
    t_m = temps / 1000
    g = -9.81

    Vprime = [0, 0]
    at = [0,0]

    vg = [0, g]

    if premiere_iteration == 0:
        premiere_iteration = 1
        vitesse = [0, 0]
        temps_precedent_position = temps
    else:
        delta_temps = t_m - t
        Vl = math.sqrt(Vx**2 + Vy**2)

        alpha = derive_hauteur_piste(X)
        sigma = math.sqrt(1 + math.pow(alpha, 2))

        v_normal = [-alpha / sigma, 1 / sigma]
        
        if(Vx < 0):
            Vu = (-1/sigma, -alpha/sigma)
        else:
            Vu = (1/sigma, alpha/sigma)

        prod_vect_vg_v_normal = vg[1] * v_normal[1]

        acc_rec = ((- prod_vect_vg_v_normal * v_normal[0]),(- prod_vect_vg_v_normal * v_normal[1]))

        Vprime[0] = Vl * Vu[0]
        Vprime[1] = Vl * Vu[1]

        at[0] = (Vprime[0] - Vx) / delta_temps
        at[1] = (Vprime[1] - Vy) / delta_temps

        acceleration_ressentie = (at[0] + acc_rec[0] , at[1] + acc_rec[1])
        norme_acceleration_ressentie = math.sqrt(acceleration_ressentie[0]**2 + acceleration_ressentie[1]**2)

        acc_frotement = ((-µc * abs(acceleration_ressentie[0] * v_normal[0] + acceleration_ressentie[1] * v_normal[1]) * Vu[0] ) , (-µc * abs(acceleration_ressentie[0] * v_normal[0] + acceleration_ressentie[1] * v_normal[1]) * Vu[1] ))

        a = (at[0] + vg[0] + acc_rec[0] + acc_frotement[0], at[1] + vg[1] + acc_rec[1] + acc_frotement[1])

        vitesse = ((Vx + delta_temps * a[0]),(Vy + delta_temps * a[1]))
    
        position_mobile = ((X + delta_temps * vitesse[0]),(Y + delta_temps * vitesse[1]))
        temps_precedent_position = temps
    
    return

def afficher_tableau_de_bord():
    acc = norme_acceleration_ressentie / 9.81
    acc_max = acceleration_max / 9.81

    vitesse_texte          = "Vitesse       : {0:.2f} m/s".format(Vl)
    vitesse_max_texte      = "Vitesse max   : {0:.2f} m/s".format(vitesse_max)
    acceleration_texte     = "Acceleration  : {0:.2f} g".format(acc)
    acceleration_max_texte = "Acceleration max : {0:.2f} g".format(acc_max)


    police = pygame.font.SysFont("monospace", 16)

    image_vitesse = police.render(vitesse_texte, True, VIOLET)
    fenetre.blit(image_vitesse,(dimensions_fenetre[0]//10,dimensions_fenetre[1]//10 - 20))
    
    image_vitesse_max = police.render(vitesse_max_texte, True, VIOLET)
    fenetre.blit(image_vitesse_max,(dimensions_fenetre[0]//10, dimensions_fenetre[1]//10 ))

    image_acceleration = police.render(acceleration_texte, True, VIOLET)
    fenetre.blit(image_acceleration, (dimensions_fenetre[0]//10, dimensions_fenetre[1]//10 + 20))

    image_acceleration_max = police.render(acceleration_max_texte, True, VIOLET)
    fenetre.blit(image_acceleration_max, (dimensions_fenetre[0]//10, dimensions_fenetre[1]//10 + 40))

def mettre_a_jour_statistiques():
    global vitesse_max, acceleration_max

    if Vl > vitesse_max:
        vitesse_max = Vl
    if norme_acceleration_ressentie > acceleration_max:
        acceleration_max = norme_acceleration_ressentie

    return

# Initialisation


pygame.init()
temps_maintenant = pygame.time.get_ticks()
temps_precedent_position = 0
Vl = 0
vitesse_max = 0
norme_acceleration_ressentie = 0
acceleration_max = 0

position_mobile = [((-dimensions_fenetre_metre[0] / 2)), hauteur_piste(-dimensions_fenetre_metre[0]/2)]

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 8")

horloge = pygame.time.Clock()
couleur_fond = JAUNEPALE

while True:
    temps_precedent = temps_maintenant
    temps_maintenant = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()   
    for t in range(temps_precedent, temps_maintenant,1):
        mettre_a_jour_position(position_mobile, t)
        mettre_a_jour_statistiques()

    fenetre.fill(couleur_fond)
    dessiner_piste()
    dessiner_mobile(position_mobile)
    afficher_tableau_de_bord()

    pygame.display.flip()
    horloge.tick(images_par_seconde)