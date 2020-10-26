
import pygame as py
from Blocks_Settings import *

vc = py.math.Vector2

class Blocky(py.sprite.Sprite):
    def __init__(self, game):
        py.sprite.Sprite.__init__(self)
        self.game = game
        self.image = py.Surface((30,40))
        self.image.fill(light_gray)
        self.rect = self.image.get_rect()
        self.rect.center = (w / 2, h / 2)
        self.pos = vc(w / 2, h / 2)
        self.vl = vc(0,0)
        self.ac = vc(0,0)

    def p_jumping(self):
        self.rect.x += 1
        hits = py.sprite.spritecollide(self,self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vl.y = -S_jump

    def update(self):
        self.ac = vc(0,S_grav)
        keys = py.key.get_pressed()
        if keys[py.K_LEFT]:
            self.ac.x= -S_ac
        if keys[py.K_RIGHT]:
            self.ac.x = S_ac

        self.ac.x += self.vl.x * S_friction

        self.vl += self.ac
        self.pos += self.vl + 0.5 * self.ac

        if self.pos.x > w:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = w

        self.rect.midbottom = self.pos

class Platform(py.sprite.Sprite):
    def __init__(self, x, y, width, height):
        py.sprite.Sprite.__init__(self)
        self.image = py.Surface((width,height))
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y