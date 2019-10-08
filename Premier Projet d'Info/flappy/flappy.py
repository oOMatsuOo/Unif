import pygame

BLEU_CIEL = (135, 206, 250)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FLAPPY_LARGEUR = 60
FLAPPY_HAUTEUR = 51

### Definition Mouvement ###

def mouvement(nom, duree):
    return (nom, duree) # durée en msec

def nomMouvement(mvt):
    return mvt[0]

def dureeMouvement(mvt):
    return mvt[1]

### Fin Entite ###

def nouvelleAnimation():
    return {
        'boucle':False,
        'repetition':0,
        'momentMouvementSuivant':None,
        'indexMouvement':None,
        'choregraphie':[] # Liste de mouvements
    }



def nouvelleEntite():
    return{
        'visible':False,
        'position':[0, 0],
        'imageAffichee':None,
        'poses':{} #dictionnaire de nom:image
    }

def visible(entite):
    entite['visible'] = True

def invisible(entite):
    entite['visible'] = False 

def estVisible(entite):
    return entite['visible']

def place(entite, x, y):
    entite['position'][0] = x
    entite['position'][1] = y

def position(entite):
    return entite['position']

def ajoutePose(entite,nom, image):
    entite['poses'][nom] = image

def prendsPose(entite, nom_pose):
    entite['imageAffichee'] = entite['poses'][nom_pose]
    visible(entite)

def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])

### fin ENTITE ###

def affiche(entites, ecran):
    for objet in entites:
        if estVisible(objet):
            dessine(objet, ecran)

pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('FLAPPY')

oiseau = nouvelleEntite()
for nom_image, nom_fichier in (('AILE_HAUTE','bird_wing_up.png'),
                    ('AILE_MILIEU','bird_wing_mid.png'),
                    ('AILE_BASSE', 'bird_wing_down.png')):
    chemin = 'images/' + nom_fichier
    image = pygame.image.load(chemin).convert_alpha(fenetre)
    image = pygame.transform.scale(image, (FLAPPY_LARGEUR, FLAPPY_HAUTEUR))
    ajoutePose(oiseau,nom_image, image)

sequence = ('AILE_MILIEU', 'AILE_HAUTE', 'AILE_MILIEU', 'AILE_BASSE')
pose = 0

place(oiseau, 50, 50)

scene = [oiseau]
attente = 0

fini = False
temps = pygame.time.Clock()

while not fini:
    # --- Traiter entrées joueur
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
    
    fenetre.fill(BLEU_CIEL)
    attente += 1
    if attente == 6:
        pose = (pose + 1) % len(sequence)
        prendsPose(oiseau, sequence[pose])
        attente = 0

    affiche(scene, fenetre)
    pygame.display.flip()

    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()