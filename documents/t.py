import pygame
import sys
import random
import time
import space  # Assurez-vous que votre fichier space.py est présent et correctement défini.

# Initialiser Pygame
pygame.init()

# Fenêtre de jeu
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
fond = pygame.image.load('background.png')

# Définir des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Variables pour la gestion du menu
menu_active = True
choisir_personnage = False
game_active = False
game_restart_timer = 10
start_time = None
pause = False
# Création des joueurs (par défaut vaisseau1)
player = space.Joueur()
player2 = space.Joueur2()
tir = space.Balle(player)
tir.etat = "chargee"
tir2 = space.Balle(player2)
tir2.etat = "chargee"

# Fonction pour afficher du texte
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Fonction pour afficher un bouton
def draw_button(text, font, color, surface, x, y, w, h):
    pygame.draw.rect(surface, color, (x, y, w, h))
    draw_text(text, font, BLACK, surface, x + 10, y + 10)

# Menu Principal
def main_menu():
    global menu_active, game_active, choisir_personnage, player, player2, tir, tir2, start_time

    while menu_active:
        
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
                        start_time = None  # Réinitialiser le timer
                        game_loop()  # Lancer le jeu
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
                        start_time = None  # Réinitialiser le timer
                        game_loop()
                    elif 225 <= mouse_pos[1] <= 275:
                        player = space.Joueur2()
                        player2 = space.Joueur()
                        choisir_personnage = False
                        game_active = True
                        start_time = None  # Réinitialiser le timer
                        game_loop()
                    elif 300 <= mouse_pos[1] <= 350:
                        choisir_personnage = False
                        menu_active = True
                        main_menu()

# Crédits
def credits_menu():
    screen.fill(BLACK)
    font = pygame.font.SysFont("monospace", 36)
    draw_text("Shems Invaders -Crédits:", font, WHITE, screen, 20, 50)
    draw_text("Développé par:", font, WHITE, screen, 200, 150)
    draw_text("HOUTMAN shems", font, WHITE, screen, 250, 200)
    draw_text("(aider par chat gpt)", font, WHITE, screen, 250, 250)
    draw_text("Appuyez sur Echap pour revenir", font, WHITE, screen, 150, 350)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# Lancer la partie
def game_loop():
    global game_active, player, player2, tir, tir2, start_time, game_restart_timer

    # Réinitialiser les variables du jeu avant de commencer
    player.score = 0
    player2.score = 0
    NbEnnemis = random.randint(3, 10)
    listeEnnemis = [space.Ennemi() for _ in range(NbEnnemis)]
    tir.etat = "chargee"
    tir2.etat = "chargee"

    while game_active:
        screen.blit(fond, (0, 0))
                   # Déplacer et afficher les joueurs
        player.deplacer()
        screen.blit(player.image, [player.position, 500])
        player2.deplacer()
        screen.blit(player2.image, [player2.position, 500])

        # Afficher les balles
        tir.bouger()
        screen.blit(tir.image, [tir.depart, tir.hauteur])
        tir2.bouger()
        screen.blit(tir2.image, [tir2.depart, tir2.hauteur])

        # Afficher les ennemis
        for ennemi in listeEnnemis:
            ennemi.avancer()  # Déplacer l'ennemi
            screen.blit(ennemi.image, (ennemi.depart, ennemi.hauteur))  
            
            if tir.toucher(ennemi):  # Vérifier si la balle touche un ennemi
                print("Un ennemi a été touché !")
                ennemi.disparaitre()  # L'ennemi disparaît
                player.marquer()  # Le joueur marque un point
            
            if tir2.toucher(ennemi):  # Vérifier si la balle de l'autre joueur touche un ennemi
                print("Un ennemi a été touché !")
                ennemi.disparaitre()  # L'ennemi disparaît
                player2.marquer()  # L'autre joueur marque un point

        pygame.display.update()  # Mettre à jour l'écran   
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
            
        # Si un joueur atteint le score de 20, on commence à gérer la fin de la partie
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
                game_active = False  # Fin du jeu
            else:
                # Afficher le timer
                elapsed_time = time.time() - start_time
                remaining_time = max(0, game_restart_timer - int(elapsed_time))
                timer_display = pygame.font.SysFont("monospace", 32).render(
                    f"Temps restant : {remaining_times}", True, (255, 0, 0)
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

        else:
            # Ajoutez ici la logique pour afficher les ennemis et les tirs

            pygame.display.update()

# Démarrer le jeu
main_menu()

