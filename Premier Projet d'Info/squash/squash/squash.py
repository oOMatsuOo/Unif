import pygame  #Utilise fonctionnalités de pygame

H = 0
V = 1
balle_vitesse = [5, 5]

fini = False

BLEU_CLAIR = ( 0, 191, 200) #Crée variable Bleu clair ( MAJ parce que la valeur ne change pas) ( ( .. , .. , ..) est une manière de représenter une couleur)
JAUNE = ( 255, 255, 0) #Crée varianle jaune ( Notation ( .., .., ..) est une TULPE, -> "Séquence immuable" val. ne peut pas changer et taille de séquence est fixe

FENETRE_LARGEUR = 1920 #Crée une variable fenetre largeur
FENETRE_HAUTEUR = 1080 #Crée une variable fenetre hauteur

BALLE_RAYON = 100

pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(BLEU_CLAIR)

balle_position = [10, 300] #Liste -> séquence mutable de valeurs

pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
pygame.display.flip()

for x in range(0, 10000): #range (b) -> séquence de 0à b-1 inclus / range (a, b) -> séquence de a à b-1 / range (a, b, s) -> séquence de a à b-1 par pallier de s.
  for evenement in pygame.event.get():
      if evenement.type == pygame.QUIT:
          fini = True
  if fini :
      pygame.display.quit()
      pygame.quit()
    
  fenetre.fill(BLEU_CLAIR)
  
  balle_position[H] = balle_position[H] + balle_vitesse[H]
  balle_position[V] = balle_position[V] + balle_vitesse[V]

  if balle_position[H] >= FENETRE_LARGEUR + BALLE_RAYON:
      balle_position[H] = -BALLE_RAYON
  if balle_position[V] >= FENETRE_HAUTEUR + BALLE_RAYON:
      balle_position[V] = -BALLE_RAYON
  
  pygame.draw.circle(fenetre, JAUNE, balle_position, BALLE_RAYON)
  pygame.display.flip()
  pygame.time.wait(1)

pygame.time.wait(5)
  
pygame.display.quit()
pygame.quit()
