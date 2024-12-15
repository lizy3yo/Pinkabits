import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, offset_x = 445, offset_y=170):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x, self.y = x, y
        self.offset_x = offset_x 
        self.offset_y = offset_y
        self.image = pygame.Surface((TILESIZE, TILESIZE))    
        self.text = text
        self.rect = self.image.get_rect()
       
        if self.text != "empty":
            self.font = pygame.font.SysFont("Press Start 2P", 25)
            font_surface = self.font.render(self.text, True, BLACK)


            if self.y == 0:  # 1st horizontal (top row)
                bg_image = pygame.image.load("tiles/azure.png")
                self.image.blit(bg_image, (0, 0))
            elif self.y == 1:  # 2nd horizontal
                bg_image = pygame.image.load("tiles/orange.png")
                self.image.blit(bg_image, (0, 0))
            elif self.y == 2:  # 3rd horizontal
                bg_image = pygame.image.load("tiles/red.png")
                self.image.blit(bg_image, (0, 0))
            elif self.y == 3:  # 4th horizontal
                bg_image = pygame.image.load("tiles/violet.png")
                self.image.blit(bg_image, (0, 0))
            elif self.y == 4:  # 4th horizontal
                bg_image = pygame.image.load("tiles/yellow.png")
                self.image.blit(bg_image, (0, 0))
           
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.bg_image = pygame.image.load("tiles/black.png")  # Load image for empty tiles
            self.image.blit(self.bg_image, (0, 0))
        
        self.rect.topleft = (self.x + self.offset_x, self.y + self.offset_y)
            

    def update(self):
        self.rect.x = self.offset_x + self.x * TILESIZE
        self.rect.y = self.offset_y + self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom
    
    def right(self):
        return self.rect.x + TILESIZE < self.offset_x + self.game.game_size * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= self.offset_x

    def up(self):
        return self.rect.y - TILESIZE >= self.offset_y

    def down(self):
        return self.rect.y + TILESIZE < self.offset_y + self.game.game_size * TILESIZE


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text, width, height):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.text = text
        self.font = pygame.font.SysFont("Press Start 2P", 12)
        font_surface = self.font.render(self.text, True, WHITE)

        self.image = pygame.image.load("buttons/buttons.png")
        self.image = pygame.transform.scale(self.image, (width, height))  # Scale the image to the button's size
        self.rect = self.image.get_rect()
        
        self.font_size = self.font.size(self.text)
        draw_x = (width / 2) - self.font_size[0] / 2
        draw_y = (height / 2) - self.font_size[1] / 2
        self.image.blit(font_surface, (draw_x, draw_y))

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen, font_size):
        font = pygame.font.SysFont("Press Start 2P", 15)
        text = font.render(self.text, True, BLACK)
        screen.blit(text, (self.x, self.y))
