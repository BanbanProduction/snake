import sys
import random
import pygame


class Jeu:
    def __init__(self):
        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Jeu Snake")
        self.jeu_en_cours = False
        self.game = True

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0
        self.serpent_corps = 10
        self.clock = pygame.time.Clock()
        self.clock_tick = 25

        self.positions_serpent = []
        self.taille_du_serpent = 1

        self.pomme_position_x = random.randrange(120, 680, 10)
        self.pomme_position_y = random.randrange(110, 580, 10)
        self.pomme_or_position_x = random.randrange(120, 680, 10)
        self.pomme_or_position_y = random.randrange(120, 580, 10)
        self.pomme = 10
        self.pomme_or_ou_pas = 100

        self.ecran_du_debut = True

        self.image_tete_du_serpent = pygame.image.load('assets/Tete_du_serpent_Vert.png')

        self.image = pygame.image.load('assets/snake-game.jpg')
        self.image_titre = pygame.transform.scale(self.image, (250, 200))

        self.score = 0

        self.boutton_facile = (60, 425, 200, 50, "Facile")
        self.boutton_moyen = (300, 425, 200, 50, "Moyen")
        self.boutton_difficile = (540, 425, 200, 50, "Difficile")
        self.boutton_recommencer = (257, 180, 285, 50, "Recommencer")
        self.boutton_quitter = (257, 370, 285, 50, "Quitter")

        self.blanc = (255, 255, 255)

    def fonction_principale(self):

        while self.game:

            if self.ecran_du_debut:
                self.ecran.fill((0, 0, 0))

                self.ecran.blit(self.image_titre, (270, 25, 100, 50))
                self.creer_message('petite', "Le but du jeu est que le serpent se développe",
                                   (85, 200, 200, 5), (240, 240, 240))
                self.creer_message('petite', "Pour cela, il a besoin de pommes, mangez-en autant que possible !",
                                   (10, 220, 200, 5), (240, 240, 240))
                self.creer_message('grande', "Choissisez la difficulté du jeu",
                                   (160, 350, 200, 5), self.blanc)
                self.creer_boutton('immense', "Facile", (60, 425, 200, 50), (100, 433, 200, 50), self.blanc,
                                   (0, 0, 0))
                self.creer_boutton('immense', "Moyen", (300, 425, 200, 50), (340, 433, 200, 50), self.blanc,
                                   (0, 0, 0))
                self.creer_boutton('immense', "Difficile", (540, 425, 200, 50), (565, 433, 200, 50), self.blanc,
                                   (0, 0, 0))

                self.tableau_score()

                self.boutton_difficulte_click()
                pygame.display.flip()

            if self.jeu_en_cours:

                self.serpent_mouvement()
                self.manger_pomme()

                la_tete_du_serpent = [self.serpent_position_x, self.serpent_position_y]
                self.positions_serpent.append(la_tete_du_serpent)

                if len(self.positions_serpent) > self.taille_du_serpent:
                    self.positions_serpent.pop(0)

                self.clock.tick(self.clock_tick)
                print(self.positions_serpent)
                self.afficher_les_elements()
                pygame.display.flip()

                self.se_mord(la_tete_du_serpent)

                if self.serpent_position_x <= 100 or self.serpent_position_x >= 700 \
                        or self.serpent_position_y <= 100 or self.serpent_position_y >= 600:
                    self.ecran_mort()

    def serpent_mouvement(self):

        for evenement in pygame.event.get():

            self.gestion_evenements(evenement)

            if evenement.type == pygame.KEYDOWN:

                if (
                    evenement.key == pygame.K_RIGHT
                    and self.serpent_direction_x != -10
                ):
                    self.serpent_direction_x = 10
                    self.serpent_direction_y = 0

                elif (
                    evenement.key == pygame.K_LEFT
                    and self.serpent_direction_x != 10
                ):
                    self.serpent_direction_x = -10
                    self.serpent_direction_y = 0

                elif (
                    evenement.key == pygame.K_DOWN
                    and self.serpent_direction_y != -10
                ):
                    self.serpent_direction_y = 10
                    self.serpent_direction_x = 0

                elif evenement.key == pygame.K_UP and self.serpent_direction_y != 10:
                    self.serpent_direction_y = -10
                    self.serpent_direction_x = 0

        self.serpent_position_x += self.serpent_direction_x
        self.serpent_position_y += self.serpent_direction_y

    def afficher_les_elements(self):
        self.ecran.fill((0, 0, 0))

        self.creer_message('grande', "Snake Game", (320, 10, 100, 50), (20, 220, 20))
        self.creer_message('grande', str(self.score), (410, 50, 50, 50), (20, 220, 20))

        pygame.draw.rect(self.ecran, self.blanc, (100, 100, 600, 500), 3)

        pygame.draw.rect(self.ecran, (255, 0, 0), (self.pomme_position_x, self.pomme_position_y,
                                                   self.pomme, self.pomme))

        if self.pomme_or_ou_pas <= 15:
            pygame.draw.rect(self.ecran, (239, 229, 19), (self.pomme_or_position_x, self.pomme_or_position_y,
                                                          self.pomme, self.pomme))

        self.ecran.blit(self.image_tete_du_serpent, (self.serpent_position_x, self.serpent_position_y,
                                                     self.serpent_corps, self.serpent_corps))

        for partie_du_serpent in self.positions_serpent[:-1]:
            pygame.draw.rect(self.ecran, (0, 255, 0), (partie_du_serpent[0], partie_du_serpent[1],
                                                       self.serpent_corps, self.serpent_corps))

    def se_mord(self, tete_serpent):

        for partie_du_serpent in self.positions_serpent[:-1]:

            if tete_serpent == partie_du_serpent:
                self.ecran_mort()

    def creer_message(self, font, message, message_rectangle, couleur):

        if font == 'petite':
            font = pygame.font.SysFont('Lato', 25)

        elif font == 'moyenne':
            font = pygame.font.SysFont('Lato', 30)

        elif font == 'grande':
            font = pygame.font.SysFont('Lato', 40, True)

        elif font == 'immense':
            font = pygame.font.SysFont('Lato', 50, True)

        message = font.render(message, True, couleur)

        self.ecran.blit(message, message_rectangle)

    def creer_boutton(self, font, texte, boutton_rectangle, texte_rectangle, couleur_boutton, couleur_texte):
        pygame.draw.rect(self.ecran, couleur_boutton, boutton_rectangle)
        self.creer_message(font, texte, texte_rectangle, couleur_texte)

    def boutton_difficulte_click(self):

        for evenement in pygame.event.get():

            self.gestion_evenements(evenement)

            if evenement.type == pygame.MOUSEBUTTONDOWN:
                x, y = evenement.pos  # the x and y coordinates of the cursor position where the mouse was clicked

                if self.boutton_facile[0] <= x <= self.boutton_facile[0] + self.boutton_facile[2] \
                        and self.boutton_facile[1] <= y <= self.boutton_facile[1] + self.boutton_facile[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True

                    self.clock_tick = 15

                elif self.boutton_moyen[0] <= x <= self.boutton_moyen[0] + self.boutton_moyen[2] \
                        and self.boutton_moyen[1] <= y <= self.boutton_moyen[1] + self.boutton_moyen[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True
                    self.clock_tick = 25

                elif self.boutton_difficile[0] <= x <= self.boutton_difficile[0] + self.boutton_difficile[2] \
                        and self.boutton_difficile[1] <= y <= self.boutton_difficile[1] + self.boutton_difficile[3]:

                    self.ecran_du_debut = False
                    self.jeu_en_cours = True
                    self.clock_tick = 35

    @staticmethod
    def gestion_evenements(evenement):

        if evenement.type == pygame.QUIT:
            sys.exit()

    def manger_pomme(self):

        if self.pomme_or_position_y == self.serpent_position_y and self.pomme_or_position_x == self.serpent_position_x \
                and self.pomme_or_ou_pas <= 15:
            self.pomme_or_ou_pas = 100
            self.pomme_or_position_x = random.randrange(120, 680, 10)
            self.pomme_or_position_y = random.randrange(120, 580, 10)

            self.taille_du_serpent += 2
            self.score += 2

        if self.pomme_position_y == self.serpent_position_y and self.pomme_position_x == self.serpent_position_x:
            self.pomme_or_ou_pas = random.randrange(0, 100, 1)
            print(self.pomme_or_ou_pas)

            self.pomme_position_x = random.randrange(120, 680, 10)
            self.pomme_position_y = random.randrange(120, 580, 10)

            self.taille_du_serpent += 1
            self.score += 1

    def recommencer(self):
        self.enregistrer_score()

        self.serpent_position_x = 300
        self.serpent_position_y = 300
        self.serpent_direction_x = 0
        self.serpent_direction_y = 0

        self.positions_serpent = []
        self.taille_du_serpent = 0
        self.score = 0

        self.jeu_en_cours = False
        self.ecran_du_debut = True

    def ecran_mort(self):

        while self.jeu_en_cours:
            self.ecran.fill((0, 0, 0))
            self.creer_boutton('immense', "Recommencer", (257, 180, 285, 50), (263, 188, 200, 50), (20, 150, 20),
                               (0, 0, 0))
            self.creer_boutton('immense', "Quitter", (257, 370, 285, 50), (325, 378, 200, 50), (20, 150, 20),
                               (0, 0, 0))
            self.bouton_mort_click()
            pygame.display.flip()

    def bouton_mort_click(self):

        for evenement in pygame.event.get():
            self.gestion_evenements(evenement)

            if evenement.type == pygame.MOUSEBUTTONDOWN:

                x, y = evenement.pos

                if self.boutton_recommencer[0] <= x <= self.boutton_recommencer[0] + self.boutton_recommencer[2] \
                        and self.boutton_recommencer[1] <= y <= \
                        self.boutton_recommencer[1] + self.boutton_recommencer[3]:

                    self.recommencer()

                elif self.boutton_quitter[0] <= x <= self.boutton_quitter[0] + self.boutton_quitter[2] \
                        and self.boutton_quitter[1] <= y <= self.boutton_quitter[1] + self.boutton_quitter[3]:
                    self.enregistrer_score()
                    sys.exit()

    def enregistrer_score(self):

        with open("Scores.txt", "a+") as file:
            file.write(str(self.score) + "\n")
            file.close()

    def tableau_score(self):

        with open("Scores.txt", "r+") as file:
            scores_liste = file.readlines()
            scores_liste = [int(score.strip()) for score in scores_liste]
            scores_liste.sort()
            scores_liste.reverse()
            del scores_liste[10:]
            file.close()

        tableau_cases_gauche = [600, 50, 20, 20]
        tableau_cases_centre = [600, 50, 120, 20]
        nombres_gauche = [605, 52, 20, 20]

        for nombre_cases in range(11):
            pygame.draw.rect(self.ecran, self.blanc, tableau_cases_gauche, 2, 5)
            pygame.draw.rect(self.ecran, self.blanc, tableau_cases_centre, 2, 5)

            if nombre_cases == 0:
                pass
            elif nombre_cases == 10:
                self.creer_message('petite', str(nombre_cases), (tableau_cases_gauche[0],
                                                                 tableau_cases_gauche[1] + 2,
                                                                 tableau_cases_gauche[2], tableau_cases_gauche[3]),
                                   self.blanc)

            else:
                self.creer_message('petite', str(nombre_cases), nombres_gauche, self.blanc)

            tableau_cases_gauche[1] += tableau_cases_gauche[3]
            tableau_cases_centre[1] += tableau_cases_centre[3]
            nombres_gauche[1] += nombres_gauche[3]

        self.creer_message('petite', "Scoreboard", (621, 51), self.blanc)

        scores_position = [655, 72]

        for score in scores_liste:
            self.creer_message('petite', str(score), scores_position, self.blanc)
            scores_position[1] += 20


if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()
