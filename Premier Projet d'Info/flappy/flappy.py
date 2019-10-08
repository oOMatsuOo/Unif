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

### Definition Animation ###

def nouvelleAnimation():
    return {
        'boucle':False,
        'repetition':0,
        'momentMouvementSuivant':None,
        'indexMouvement':None,
        'choregraphie':[] # Liste de mouvements
    }

def repete(animation, fois):
    animation['repetition'] = fois
    animation['boucle'] = False

def enBoucle(animation):
    animation['boucle'] = True

def ajouteMouvement(animation, mvt):
    animation['choregraphie'].append(mvt)
    
def mouvementActuel(animation):
    if animation['indexMouvement'] == None:
        return None
    else:
        return nomMouvement(animation['choregraphie'][animation['indexMouvement']])

def commenceMouvement(animation, index):
    animation['indexMouvement'] = index
    animation['momentMouvementSuivant'] = pygame.time.get_ticks() + dureeMouvement(animation['choregraphie'][index])


def commence(animation):
    commenceMouvement(animation, 0)

def arrete(animation):
    animation['indexMouvement'] = None


def anime(animation):
    if animation['indexMouvement'] == None:
        commence(animation)
    elif animation['momentMouvementSuivant'] <= pygame.time.get_ticks():
        if animation['indexMouvement'] == len(animation['choregraphie']) - 1:
            if animation['boucle']:
                commence(animation)
            else:
                if animation['repetition'] > 0:
                    animation['repetition'] -= 1
                    commence(animation)
                else:
                    arrete(animation)
        else:
            commenceMouvement(animation, animation['indexMouvement'] + 1)

### Fin Animation ###

### Definition Entite ###

def nouvelleEntite():
    return{
        'visible':False,
        'position':[0, 0],
        'imageAffichee':None,
        'poses':{}, #dictionnaire de nom:image
        'animationActuelle':None,
        'animations':{}
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

def commenceAnimation(entite, nomAnimation, fois = 1):
    entite['animationActuelle'] = entite['animations'][nomAnimation]
    if fois == 0:
        enBoucle(entite['animationActuelle'])
    else:
        repete(entite['animationActuelle'], fois - 1)
    visible(entite)

def arreteAnimation(entite):
    arrete(entite['animationActuelle'])
    entite['animationActuelle'] = None

def ajouteAnimation(entite, nom, animation):
    entite['animations'][nom] = animation

def estEnAnimation(entite):
    return entite['animationActuelle'] != None

### fin ENTITE ###

def affiche(entites, ecran):
    for objet in entites:
        if estVisible(objet):
            if estEnAnimation(objet):
                animationActuelle = objet['animationActuelle']
                poseActuelle = mouvementActuel(animationActuelle)
                anime(animationActuelle)
                nouvellePose = mouvementActuel(animationActuelle)
                if nouvellePose == None:
                    objet['animationActuelle'] = None
                    prendsPose(objet, poseActuelle)
                else:
                    prendsPose(objet, nouvellePose)
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

animation = nouvelleAnimation()
ajouteMouvement(animation, mouvement('AILE_HAUTE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 80))
ajouteMouvement(animation, mouvement('AILE_BASSE', 80))
ajouteMouvement(animation, mouvement('AILE_MILIEU', 320))

ajouteAnimation(oiseau, 'vol', animation)

place(oiseau, 50, 50)

scene = [oiseau]
commenceAnimation(oiseau, 'vol', 0)

fini = False
temps = pygame.time.Clock()

while not fini:
    # --- Traiter entrées joueur
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
    
    fenetre.fill(BLEU_CIEL)

    affiche(scene, fenetre)
    pygame.display.flip()

    temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()