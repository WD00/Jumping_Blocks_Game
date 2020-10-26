# Jumping blocks

import pygame as py
from os import path
import random
from Blocks_Settings import *
from Blocks_Sprites import *


class Game:
    def __init__(self):

        py.init()
        py.mixer.init()
        self.screen = py.display.set_mode((w, h))
        py.display.set_caption("Jumping blocks!")
        game_icon = py.image.load('block_icon.png')
        py.display.set_icon(game_icon)
        self.clock = py.time.Clock()
        self.running = True
        self.font_name = py.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):

        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new_sprites(self):

        self.score = 0
        self.sprites = py.sprite.Group()
        self.platforms = py.sprite.Group()
        self.player = Blocky(self)
        self.sprites.add(self.player)
        for plat in game_platforms:
            p = Platform(*plat)
            self.sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):

        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.game_events()
            self.update()
            self.game_draw()

    def update(self):

        self.sprites.update()

        if self.player.vl.y > 0:
            hits = py.sprite.spritecollide(self.player, self.platforms,False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vl.y = 0

        if self.player.rect.top <= h / 4:
            self.player.pos.y += abs(self.player.vl.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vl.y)

                if plat.rect.top >= h:
                    plat.kill()
                    self.score += 1

        if self.player.rect.bottom > h:
            for sprite in self.sprites:
                sprite.rect.y -= max(self.player.vl.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 6:
            Width = random.randrange(50,100)
            p = Platform(random.randrange(0, w - Width),
                         random.randrange( -75, -30),
                         Width, 20)
            self.platforms.add(p)
            self.sprites.add(p)



    def game_events(self):

        for event in py.event.get():

            if event.type == py.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    self.player.p_jumping()


    def game_draw(self):

        self.screen.fill(background_c)
        self.sprites.draw(self.screen)
        self.game_text(str(self.score), 22, white, w / 2, 15)
        py.display.flip()

    def start_menu(self):

        self.screen.fill(black)
        self.game_text("Jumping blocks!", 40, white, w / 2, h / 4)
        self.game_text("Please use arrow keys and space to jump :)", 22, light_gray, w / 2, h / 2)
        self.game_text("Press 'A' key to start the game", 18, light_gray, w / 2, h * 3 / 4)
        self.game_text("High score:" + str(self.highscore), 22, light_gray, w / 2, 15)
        py.display.flip()
        self.wait_for_key()

    def end_game_over(self):

        if not self.running:
            return
        self.screen.fill(black)
        self.game_text("G A M E   O V E R", 40, light_gray, w / 2, h / 4)
        self.game_text("Your Score: " + str(self.score), 22, white, w / 2, h / 2)
        self.game_text("Press 'A' key to play again", 18, gray, w / 2, h * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.game_text("Congrats! New High Score!", 22, white, w / 2, h / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.game_text("High score:" + str(self.highscore), 22, white, w / 2, h / 2 + 40)
        py.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in py.event.get():
                if event.type == py.QUIT:
                    waiting = False
                    self.running = False
                if event.type == py.KEYUP:
                    waiting = False

    def game_text(self, text, size, color, x, y):
        font = py.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



g = Game()
g.start_menu()
while g.running:
    g.new_sprites()
    g.end_game_over()

py.quit()