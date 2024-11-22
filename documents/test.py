import pygame # importation de la librairie pygame
import space
import sys # pour fermer correctement l'application
import random
import time  
# lancement des modules inclus dans pygame
pygame.init() 

# création d'une fenêtre de 800 par 600
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaders") 
# chargement de l'image de fond
fond = pygame.image.load('background.png')
# Définir des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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

menu_active = True
choisir_personnage = False
game_active = False
game_restart_timer = 10
start_time = None

# Variables pour gérer le compte à rebours
game_restart_timer = 10
start_time = None
restart_game = False
pause= False
running = True
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, w, h):
    pygame.draw.rect(surface, color, (x, y, w, h))
    draw_text(text, font, BLACK, surface, x + 10, y + 10)

# Menu Principal
def main_menu():
    global menu_active, game_active, choisir_personnage
    while menu_active:
        screen.fill(WHITE)
        font = pygame.font.SysFont("monospace", 36)

        # Titre du jeu
        draw_text("Space Invaders", font, GREEN, screen, 300, 50)

        # Boutons
        draw_button("Jouer", font, GREEN, screen, 300, 150, 200, 50)
        draw_button("Choisir Personnage", font, GREEN, screen, 300, 225, 200, 50)
        draw_button("Crédits", font, GREEN, screen, 300, 300, 200, 50)
        draw_button("Quitter", font, RED, screen, 300, 375, 200, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500:
                    if 150 <= mouse_pos[1] <= 200:
                        menu_active = False
                        game_active = True
                    elif 225 <= mouse_pos[1] <= 275:
                        choisir_personnage = True
                        personnage_menu()
                    elif 300 <= mouse_pos[1] <= 350:
                        credits_menu()
                    elif 375 <= mouse_pos[1] <= 425:
                        pygame.quit()
                        sys.exit()

# Choisir son personnage
def personnage_menu():
    global choisir_personnage, player, player2
    while choisir_personnage:
        screen.fill(WHITE)
        font = pygame.font.SysFont("monospace", 36)

        # Choix de personnage
        draw_text("Choisir un personnage", font, GREEN, screen, 250, 50)
        draw_button("Vaisseau 1", font, GREEN, screen, 300, 150, 200, 50)
        draw_button("Vaisseau 2", font, GREEN, screen, 300, 225, 200, 50)
        draw_button("Retour", font, GREEN, screen, 300, 300, 200, 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500:
                    if 150 <= mouse_pos[1] <= 200:
                        player = space.Joueur()
                        player2 = space.Joueur2()
                        choisir_personnage = False
                        game_active = True
                    elif 225 <= mouse_pos[1] <= 275:
                        player = space.Joueur2()
                        player2 = space.Joueur()
                        choisir_personnage = False
                        game_active = True
                    elif 300 <= mouse_pos[1] <= 350:
                        choisir_personnage = False

# Crédits
def credits_menu():
    screen.fill(WHITE)
    font = pygame.font.SysFont("monospace", 36)
    draw_text("Space Invaders - Crédits", font, GREEN, screen, 250, 50)
    draw_text("Développé par [Votre Nom]", font, GREEN, screen, 250, 150)
    draw_text("Appuyez sur Echap pour revenir", font, GREEN, screen, 200, 250)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
def game_loop():
    global game_active, player, player2, tir, tir2
    while game_active:
        screen.blit(fond, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion des touches pour déplacer et tirer
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.sens = "gauche"
                if event.key == pygame.K_RIGHT:
                    player.sens = "droite"
                if event.key == pygame.K_UP:
                    player.tirer()
                    tir.etat = "tiree"
                if event.key == pygame.K_q:
                    player2.sens = "gauche"
                if event.key == pygame.K_d:
                    player2.sens = "droite"
                if event.key == pygame.K_SPACE:
                    player2.tirer()
                    tir2.etat = "tiree"
                if event.key == pygame.K_e:
                    pause = not pause

        # Ajoutez la logique de jeu comme vous l'aviez précédemment ici (affichage des scores, ennemis, etc.)

        pygame.display.update()
        
    while running:  # Boucle principale
        screen.blit(fond, (0, 0))  # Affichage du fond

        for event in pygame.event.get():  # Gestion des événements
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            # Gestion des touches pour déplacer et tirer
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.sens = "gauche"
                if event.key == pygame.K_RIGHT:
                    player.sens = "droite"
                if event.key == pygame.K_UP:
                    player.tirer()
                    tir.etat = "tiree"
                if event.key == pygame.K_q:
                    player2.sens = "gauche"
                if event.key == pygame.K_d:
                    player2.sens = "droite"
                if event.key == pygame.K_SPACE:
                    player2.tirer()
                    tir2.etat = "tiree"
                if event.key == pygame.K_e:
                    pause = not pause

        if pause:
            myfont_pause = pygame.font.SysFont("monospace", 32)
            pause_display = myfont_pause.render("Jeu en Pause. Appuyez sur E pour continuer.", True, (255, 255, 0))
            screen.blit(pause_display, (25, 250))
            pygame.display.update()
            continue

        if player.score >= 20 or player2.score >= 20:  # Condition de victoire
            if start_time is None:
                start_time = time.time()  # Initialisation du timer

            # Identifier gagnant et perdant
            if player.score >= 20:
                joueur_gagnant = player
                joueur_perdant = player2
                tir_gagnant = tir
            else:
                joueur_gagnant = player2
                joueur_perdant = player
                tir_gagnant = tir2

            # Déplacer et afficher les joueurs
            joueur_perdant.deplacer()
            screen.blit(joueur_perdant.image, [joueur_perdant.position, 50])
            joueur_gagnant.deplacer()
            screen.blit(joueur_gagnant.image, [joueur_gagnant.position, 500])

            # Déplacer la balle et vérifier si elle touche
            tir_gagnant.bouger()
            screen.blit(tir_gagnant.image, [tir_gagnant.depart, tir_gagnant.hauteur])

            if tir_gagnant.toucher(joueur_perdant):
                print("Le joueur perdant a été touché !")
                running = False  # Fin du jeu
            else:
                # Afficher le timer
                elapsed_time = time.time() - start_time
                remaining_time = max(0, game_restart_timer - int(elapsed_time))
                timer_display = pygame.font.SysFont("monospace", 32).render(
                    f"Temps restant : {remaining_time} s", True, (255, 0, 0)
                )
                screen.blit(timer_display, (300, 250))

                if remaining_time == 0:  # Temps écoulé
                    print("Temps écoulé, redémarrage du jeu !")
                    # Réinitialiser le jeu
                    player.score = 0
                    player2.score = 0
                    start_time = None
                    listeEnnemis = [space.Ennemi() for _ in range(NbEnnemis)]
                    tir_gagnant.etat = "chargee"

        else:  # Jeu en cours
            for ennemi in listeEnnemis:
                if tir.toucher(ennemi):
                    ennemi.disparaitre()
                    player.marquer()
                if tir2.toucher(ennemi):
                    ennemi.disparaitre()
                    player2.marquer()

            for ennemi in listeEnnemis:
                ennemi.avancer()
                screen.blit(ennemi.image, [ennemi.depart, ennemi.hauteur])

            player.deplacer()
            screen.blit(player.image, [player.position, 500])
            tir.bouger()
            screen.blit(tir.image, [tir.depart, tir.hauteur])

            player2.deplacer()
            screen.blit(player2.image, [player2.position, 500])
            tir2.bouger()
            screen.blit(tir2.image, [tir2.depart, tir2.hauteur])

        score_display = pygame.font.SysFont("monospace", 16).render(
            f"SCORE J1 = {player.score}", 1, (255, 255, 0)
        )
        screen.blit(score_display, (625, 25))
        score_display2 = pygame.font.SysFont("monospace", 16).render(
            f"SCORE J2 = {player2.score}", 1, (255, 255, 0)
        )
        screen.blit(score_display2, (25, 25))

        pygame.display.update()
