import sys
import random
import pygame


class Jeu:
    def __init__(self):
        self.difficulte = ""
        self.ecran = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake")

        self.ecran_du_debut = True
        self.ecran_scoreboards = False
        self.ecran_choix_style = False
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

        self.image = pygame.image.load('assets/snake-game.jpg')
        self.image_titre = pygame.transform.scale(self.image, (250, 200))

        self.score = 0

        self.boutton_facile = (60, 425, 200, 50)
        self.boutton_moyen = (300, 425, 200, 50)
        self.boutton_difficile = (540, 425, 200, 50)
        self.boutton_scoreboard = (20, 85, 220, 30)
        self.boutton_style = (560, 85, 220, 30)

        self.boutton_retour = (20, 85, 100, 30)

        self.boutton_recommencer = (257, 180, 285, 50)
        self.boutton_quitter = (257, 370, 285, 50)

        self.blanc = (255, 255, 255)
        self.noir = (0, 0, 0)

        self.styles = [["Blanc", self.blanc, self.noir], ["Bleu_clair", (0, 162, 232)], ["Bleu_foncé", (63, 72, 204)],
                       ["Orange", (255, 128, 0)], ["Vert", (0, 255, 0), (0, 191, 0)], ["Violet", (169, 67, 171)]]
        self.couleur_position = [125, 225]
        self.serpent_couleur = ["Vert", (0, 191, 0)]
        self.serpent_couleur[-1] = (0, 191, 0)

    def fonction_principale(self):

        while self.game:

            if self.ecran_du_debut:
                self.afficher_elements_debut()
                self.bouttons_debut_click()

                pygame.display.flip()

            if self.ecran_scoreboards:
                self.afficher_elements_scoreboards()
                self.bouttons_scoreboard_click()

                pygame.display.flip()

            if self.ecran_choix_style:
                self.afficher_elements_style()
                self.boutton_styles_click()

                pygame.display.flip()

            if self.jeu_en_cours:

                self.serpent_mouvement()
                self.manger_pomme()

                la_tete_du_serpent = [self.serpent_position_x, self.serpent_position_y]
                self.positions_serpent.append(la_tete_du_serpent)

                if len(self.positions_serpent) > self.taille_du_serpent:
                    self.positions_serpent.pop(0)

                self.afficher_elements_jeu()

                self.se_mord(la_tete_du_serpent)

                self.clock.tick(self.clock_tick)
                pygame.display.flip()

                if self.serpent_position_x <= 100 or self.serpent_position_x >= 700 \
                        or self.serpent_position_y <= 100 or self.serpent_position_y >= 600:
                    self.ecran_mort()

    def serpent_mouvement(self):

        for evenement in pygame.event.get():

            self.gestion_quitter(evenement)

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

    def afficher_elements_debut(self):

        self.ecran.fill(self.noir)

        self.ecran.blit(self.image_titre, (270, 25, 100, 50))
        self.creer_message(25, "Le but du jeu est que le serpent se développe", (205, 200, 200, 5),
                           self.serpent_couleur[1])
        self.creer_message(25, "Pour cela, il a besoin de pommes, mangez-en autant que possible !",
                           (115, 220, 200, 5), self.serpent_couleur[1])
        self.creer_message(40, "Choissisez la difficulté du jeu", (160, 350, 200, 5), self.serpent_couleur[1], True)
        self.creer_boutton(50, "Facile", self.boutton_facile, (100, 433), self.blanc, self.serpent_couleur[-1], True)
        self.creer_boutton(50, "Moyen", self.boutton_moyen, (340, 433), self.blanc, self.serpent_couleur[-1], True)
        self.creer_boutton(50, "Difficile", self.boutton_difficile, (565, 433), self.blanc, self.serpent_couleur[-1],
                           True)

        self.creer_boutton(35, "Meilleurs scores", self.boutton_scoreboard, (33, 89), self.blanc,
                           self.serpent_couleur[-1])
        self.creer_boutton(35, "Choix du style", self.boutton_style, (583, 89), self.blanc, self.serpent_couleur[-1])

    def afficher_elements_scoreboards(self):

        self.ecran.fill(self.noir)

        self.creer_boutton(35, "Retour", self.boutton_retour, (30, 89), self.blanc, self.serpent_couleur[-1])
        self.creer_message(60, "Meilleurs scores", (205, 82, 100, 30), self.serpent_couleur[1], True)

        def creer_scoreboard(difficulte, cases_gauche, cases_centre, nombres_gauche, scores_position):

            with open("Scores{}.txt".format(difficulte), "r+") as file:
                scores_liste = file.readlines()
                scores_liste = [int(score.strip()) for score in scores_liste]
                scores_liste.sort()
                scores_liste.reverse()
                del scores_liste[10:]
                file.close()

            if difficulte == "Facile":
                self.creer_message(25, str(difficulte), (cases_centre[0] + 43, cases_centre[1] + 1), self.blanc)

            elif difficulte == "Moyen":
                self.creer_message(25, str(difficulte), (cases_centre[0] + 41, cases_centre[1] + 1), self.blanc)

            elif difficulte == "Difficile":
                self.creer_message(25, str(difficulte), (cases_centre[0] + 35, cases_centre[1] + 1), self.blanc)

            nombre_cases = 0

            while nombre_cases <= 10:
                pygame.draw.rect(self.ecran, self.blanc, cases_gauche, 2, 5)
                pygame.draw.rect(self.ecran, self.blanc, cases_centre, 2, 5)

                if nombre_cases == 10:
                    self.creer_message(25, str(nombre_cases), (cases_gauche[0], cases_gauche[1] + 2,
                                                               cases_gauche[2], cases_gauche[3]), self.blanc)

                elif nombre_cases == 0:
                    pass

                else:
                    self.creer_message(25, str(nombre_cases), nombres_gauche, self.blanc)

                nombre_cases += 1
                cases_gauche[1] += cases_gauche[3]
                cases_centre[1] += cases_centre[3]
                nombres_gauche[1] += nombres_gauche[3]

            for score in scores_liste:
                self.creer_message(25, str(score), scores_position, self.blanc)
                scores_position[1] += 20

        creer_scoreboard("Facile", [110, 200, 20, 20], [110, 200, 120, 20], [115, 202, 20, 20], [168, 222])
        creer_scoreboard("Moyen", [340, 200, 20, 20], [340, 200, 120, 20], [345, 202, 20, 20], [398, 222])
        creer_scoreboard("Difficile", [570, 200, 20, 20], [570, 200, 120, 20], [575, 202, 20, 20], [628, 222])

    def afficher_elements_style(self):

        self.ecran.fill(self.noir)
        self.creer_boutton(35, "Retour", self.boutton_retour, (30, 89), self.blanc, self.serpent_couleur[-1])
        self.creer_message(60, "Choisis ton style", (205, 82, 100, 30), self.blanc, True)

        tete_position = [225, 275]
        self.couleur_position = [125, 225]

        for nombre_serpent, style in enumerate(self.styles, start=1):

            corps_position = tete_position

            tete = pygame.image.load("assets/Tete_du_serpent_{}.png".format(style[0]))
            self.ecran.blit(tete, (tete_position[0], tete_position[1], self.serpent_corps, self.serpent_corps))
            self.creer_message(40, str(style[0]), self.couleur_position, style[1], True)

            for _ in range(10):

                corps_position[0] -= 10
                pygame.draw.rect(self.ecran, style[1], (corps_position[0], corps_position[1], 10, 10))

            tete_position[0] += 300
            self.couleur_position[0] += 200

            if nombre_serpent == 3:
                tete_position[0] = 225
                tete_position[1] += 150

                self.couleur_position[0] = 125
                self.couleur_position[1] += 150

    def afficher_elements_jeu(self):
        self.ecran.fill(self.noir)

        self.creer_message(40, "Snake Game", (320, 10, 100, 50), self.serpent_couleur[-1], True)
        self.creer_message(40, str(self.score), (410, 50, 50, 50), self.serpent_couleur[-1], True)

        pygame.draw.rect(self.ecran, self.blanc, (100, 100, 600, 500), 3)

        pygame.draw.rect(self.ecran, (255, 0, 0), (self.pomme_position_x, self.pomme_position_y,
                                                   self.pomme, self.pomme))

        if self.pomme_or_ou_pas <= 15:
            pygame.draw.rect(self.ecran, (239, 229, 19), (self.pomme_or_position_x, self.pomme_or_position_y,
                                                          self.pomme, self.pomme))

        for partie_du_serpent in self.positions_serpent[:-1]:
            pygame.draw.rect(self.ecran, self.serpent_couleur[1], (partie_du_serpent[0], partie_du_serpent[1],
                             self.serpent_corps, self.serpent_corps))

        image_tete_du_serpent = pygame.image.load('assets/Tete_du_serpent_{}.png'.format(self.serpent_couleur[0]))

        self.ecran.blit(image_tete_du_serpent, (self.serpent_position_x, self.serpent_position_y,
                                                self.serpent_corps, self.serpent_corps))

    def se_mord(self, tete_serpent):

        for partie_du_serpent in self.positions_serpent[:-1]:

            if tete_serpent == partie_du_serpent:
                self.ecran_mort()

    def creer_message(self, font, message, message_rectangle, couleur, gras=False):

        font = pygame.font.SysFont('Lato', font, gras)

        message = font.render(message, True, couleur)

        self.ecran.blit(message, message_rectangle)

    def creer_boutton(self, font, text, boutton_rectangle, texte_rectangle, couleur_boutton, couleur_texte, gras=False):
        pygame.draw.rect(self.ecran, couleur_boutton, boutton_rectangle)
        self.creer_message(font, text, texte_rectangle, couleur_texte, gras)

    def bouttons_debut_click(self):

        for evenement in pygame.event.get():

            self.gestion_quitter(evenement)

            if self.boutton_click(evenement, self.boutton_facile):

                self.mettre_difficulte(15, "Facile")
            elif self.boutton_click(evenement, self.boutton_moyen):

                self.mettre_difficulte(20, "Moyen")
            elif self.boutton_click(evenement, self.boutton_difficile):

                self.mettre_difficulte(35, "Difficile")
            elif self.boutton_click(evenement, self.boutton_scoreboard):

                self.ecran_du_debut = False
                self.ecran_scoreboards = True

            elif self.boutton_click(evenement, self.boutton_style):

                self.ecran_du_debut = False
                self.ecran_choix_style = True

    def mettre_difficulte(self, tick, difficulte):
        self.ecran_du_debut = False
        self.jeu_en_cours = True

        self.clock_tick = tick
        self.difficulte = difficulte

    @staticmethod
    def gestion_quitter(evenement):

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
            self.ecran.fill(self.noir)
            self.creer_boutton(50, "Recommencer", (257, 180, 285, 50), (263, 188, 200, 50), self.serpent_couleur[-1],
                               self.noir, True)
            self.creer_boutton(50, "Quitter", (257, 370, 285, 50), (325, 378, 200, 50), self.serpent_couleur[-1],
                               self.noir, True)
            self.boutons_mort_click()
            pygame.display.flip()

    def enregistrer_score(self):

        with open("Scores{}.txt".format(self.difficulte), "a+") as file:
            file.write(str(self.score) + "\n")
            file.close()

    @staticmethod
    def boutton_click(evenement, boutton):

        if evenement.type == pygame.MOUSEBUTTONDOWN:
            x, y = evenement.pos

            return (
                boutton[0] <= x <= boutton[0] + boutton[2]
                and boutton[1] <= y <= boutton[1] + boutton[3]
            )

    def bouttons_scoreboard_click(self):

        for evenement in pygame.event.get():

            self.gestion_quitter(evenement)

            if self.boutton_click(evenement, self.boutton_retour):
                self.ecran_du_debut = True
                self.ecran_scoreboards = False
                self.ecran_choix_style = False

    def boutton_styles_click(self):

        for evenement in pygame.event.get():

            self.gestion_quitter(evenement)

            if self.boutton_click(evenement, self.boutton_retour):
                self.ecran_du_debut = True
                self.ecran_choix_style = False

            self.couleur_position = [125, 225, 110, 70]

            for nombre_styles, style in enumerate(self.styles, start=1):

                if self.boutton_click(evenement, self.couleur_position):
                    self.serpent_couleur = style
                    self.ecran_du_debut = True
                    self.ecran_choix_style = False

                self.couleur_position[0] += 200
                if nombre_styles == 3:
                    self.couleur_position[0] = 125
                    self.couleur_position[1] += 150

    def boutons_mort_click(self):

        for evenement in pygame.event.get():

            self.gestion_quitter(evenement)

            if self.boutton_click(evenement, self.boutton_recommencer):

                self.recommencer()

            elif self.boutton_click(evenement, self.boutton_quitter):

                self.enregistrer_score()
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    Jeu().fonction_principale()
    pygame.quit()