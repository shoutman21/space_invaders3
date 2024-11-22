import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application
import random

# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders") 
# chargement de l'image de fond
fond = pygame.image.load('background.png')

# creation du joueur
player = space.Joueur()
player2 = space.Joueur2()
# creation de la balle
tir = space.Balle(player)
tir.etat = "chargee"
tir2 = space.Balle(player2)
tir2.etat = "chargee"
# creation des ennemis
NbEnnemis=random.randint(3,10)
listeEnnemis = []
for indice in range(NbEnnemis):
    vaisseau = space.Ennemi()
    listeEnnemis.append(vaisseau)


### BOUCLE DE JEU  ###
pause= False
running = True # variable pour laisser la fenêtre ouverte

while running : # boucle infinie pour laisser la fenêtre ouverte
    # dessin du fond
    screen.blit(fond,(0,0))

    ### Gestion des événements  ###
    for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
        if event.type == pygame.QUIT : # si l'événement est le clic sur la fermeture de la fenêtre
            running = False # running est sur False
            sys.exit() # pour fermer correctement
       
       # gestion du clavier
        if event.type == pygame.KEYDOWN : # si une touche a été tapée KEYUP quand on relache la touche
            if event.key == pygame.K_LEFT : # si la touche est la fleche gauche
                player.sens = "gauche" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_RIGHT : # si la touche est la fleche droite
                player.sens = "droite" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_UP : # espace pour tirer
                player.tirer()
                tir.etat = "tiree"
            if event.key == pygame.K_q : # si la touche est la fleche gauche
                player2.sens = "gauche" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_d : # si la touche est la fleche droite
                player2.sens = "droite" # on déplace le vaisseau de 1 pixel sur la gauche
            if event.key == pygame.K_SPACE : # espace pour tirer
                player2.tirer()
                tir2.etat = "tiree"
            if event.key == pygame.K_e:
                pause = not pause
    if pause:
        myfont_pause = pygame.font.SysFont("monospace", 32)
        pause_display = myfont_pause.render("Jeu en Pause. Appuyez sur E pour continuer.", True, (255, 255, 0))
        screen.blit(pause_display, (25, 250))  # Position du message
        pygame.display.update()  # Mettre à jour l'écran
        continue
    

    ### Actualisation de la scene ###
    # Gestions des collisions et des conditions de victoire
    if player.score >= 20 or player2.score >= 20:  # Si un des joueurs atteint un score de 20
        listeEnnemis = []
        
        if player.score >= 20:  # Le joueur 1 a gagné
            joueur_gagnant = player
            joueur_perdant = player2
            tirp= tir2
            tirg= tir
        else:  # Le joueur 2 a gagné
            joueur_gagnant = player2
            joueur_perdant = player
            tirp=tir
            tirg=tir2

        # Déplacer le joueur perdant en haut de l'écran
        
        
        joueur_perdant.deplacer()
        screen.blit(joueur_perdant.image, [joueur_perdant.position, 50])
        # Afficher le joueur gagnant à sa position normale
        joueur_gagnant.deplacer()
        screen.blit(joueur_gagnant.image, [joueur_gagnant.position, 500])
         # Afficher la balle et la déplacer
        tirg.bouger()
        screen.blit(tirg.image, [tirg.depart, tirg.hauteur])
        tirp.bouger()
        screen.blit(tirp.image, [tirp.depart, 50])
        # Tirer sur le joueur perdant
        if tirg.toucher(joueur_perdant) :
            print("Le joueur perdant a été touché !")
        
    else:  # Si aucun joueur n'a encore atteint un score de 20
    # Gestions des collisions des ennemis
        for ennemi in listeEnnemis:
            if tir.toucher(ennemi):  # collision pour le joueur 1
                ennemi.disparaitre()
                player.marquer()
            if tir2.toucher(ennemi):  # collision pour le joueur 2
                ennemi.disparaitre()
                player2.marquer()

        # Les ennemis continuent d'avancer
        for ennemi in listeEnnemis:
            ennemi.avancer()
            screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])  # Affichage des ennemis
        # placement des objets
        # le joueur
        player.deplacer()
        screen.blit(tir.image,[tir.depart,tir.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur    
        player2.deplacer()
        screen.blit(tir2.image,[tir2.depart,tir2.hauteur])
        # la balle
        tir.bouger()
        screen.blit(player.image,[player.position,500]) # appel de la fonction qui dessine le vaisseau du joueur
        tir2.bouger()
        screen.blit(player2.image,[player2.position,500])
    #création d'un tableau score
    score = player.score
    myfont = pygame.font.SysFont("monospace", 16)
    score_display = myfont.render(("SCORE J1 = "+str(score)), 1, (255,255,0))
    screen.blit(score_display, (625, 25))
    
    score2 = player2.score
    myfont2 = pygame.font.SysFont("monospace", 16)
    score_display2 = myfont2.render(("SCORE J2 = "+str(score2)), 1, (255,255,0))
    screen.blit(score_display2, (25, 25))
    # les ennemis
    for ennemi in listeEnnemis:
        ennemi.avancer()
        screen.blit(ennemi.image,[ennemi.depart, ennemi.hauteur]) # appel de la fonction qui dessine le vaisseau du joueur
        
    pygame.display.update() # pour ajouter tout changement à l'écran
