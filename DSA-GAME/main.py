import time
import pygame
from settings import *
from sprites import *
import random
import time


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(400, 100)
        self.start_shuffle = False
        self.shuffle_time = 0
        self.previous_choice = ""
        self.choice = ""
        self.start_timer = False
        self.start_game = False
        self.elapsed_time = 0
        self.tiles = []
        self.high_score_easy = float(self.get_high_scores()[0])
        self.high_score_medium = float(self.get_high_scores()[1])
        self.high_score_hard = float(self.get_high_scores()[2])
        
        self.background_image = pygame.image.load("photos/background.png")  # Make sure this file is in your directory
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))  # Resize if necessary

    def get_high_scores(self):
        with open("high_scores.txt", "r") as file:
            scores = file.read().splitlines()
        return scores

    def save_score(self):
        with open("high_scores.txt", "w") as file:
            file.write(str("%.3f\n" % self.high_score_easy))
            file.write(str("%.3f\n" % self.high_score_medium))
            file.write(str("%.3f" % self.high_score_hard))

    def create_game(self, game_size):
        grid = [[x + y * game_size for x in range(1, game_size + 1)] for y in range(game_size)]
        grid[-1][-1] = 0
        return grid
    

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        self.choice = random.choice(possible_moves)
        self.previous_choice = self.choice
        if self.choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif self.choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif self.choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif self.choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game(self.game_size)
        self.tiles_grid_completed = self.create_game(self.game_size)
        self.elapsed_time = 0
        self.moves = 0
        self.start_timer = False
        self.start_game = False
        self.draw_buttons()
        self.draw_tiles()
        

    def draw_timer(self, timer):
        UIElement(340, 130, timer).draw(self.screen, 40)

    def draw_high_score(self, score):
        UIElement(550, 132, score).draw(self.screen, 30)

    def draw_buttons(self):
        
        self.buttons_list = []
        self.buttons_list.append(Button(self, 575, 475, "SHUFFLE", 160, 50,))
        self.buttons_list.append(Button(self, 475, 475, "RESET", 110, 50))
        self.buttons_list.append(Button(self, 350, 575, "EASY", 100, 50))
        self.buttons_list.append(Button(self, 500, 575, "MEDIUM", 150, 50))
        self.buttons_list.append(Button(self, 700, 575, "HARD", 100, 50))

    def draw_tiles(self):
        self.tiles = []
        
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()

    def update(self):
        # print(self.clock.get_fps())
        # update portion of the game loop
        if self.start_game:
            # check if game is completed
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
                if self.game_choice == EASY:
                    if self.high_score_easy > 0:
                        self.high_score_easy = self.elapsed_time if self.elapsed_time < self.high_score_easy else self.high_score_easy
                    else:
                        self.high_score_easy = self.elapsed_time
                elif self.game_choice == MEDIUM:
                    if self.high_score_medium > 0:
                        self.high_score_medium = self.elapsed_time if self.elapsed_time < self.high_score_medium else self.high_score_medium
                    else:
                        self.high_score_medium = self.elapsed_time
                elif self.game_choice == HARD:
                    if self.high_score_hard > 0:
                        self.high_score_hard = self.elapsed_time if self.elapsed_time < self.high_score_hard else self.high_score_hard
                    else:
                        self.high_score_hard = self.elapsed_time
                self.save_score()

            if self.start_timer:
                self.timer = time.time()
                self.start_timer = False
            self.elapsed_time = time.time() - self.timer

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 100:
                self.start_shuffle = False
                self.start_timer = True
                self.start_game = True
                
        self.all_sprites.update()

    def draw_grid(self, offset_x= 445, offset_y=170):
    # Draw the grid lines on the screen based on the game size, with an offset for positioning
        for row in range(-1, self.game_choice, TILESIZE):
          pygame.draw.line(self.screen, LIGHTGREY, (offset_x + row, offset_y), (offset_x + row, offset_y + self.game_choice))
        for col in range(-1, self.game_choice, TILESIZE):
          pygame.draw.line(self.screen, LIGHTGREY, (offset_x, offset_y + col), (offset_x + self.game_choice, offset_y + col))

            
            
    def draw(self):
        # Fill the screen with the background image
        self.screen.blit(self.background_image, (0, 0))  # Draw the background image

        # Now draw other elements (like grid, buttons, timer, etc.)
        self.all_sprites.draw(self.screen)
        self.draw_grid()

        if self.game_choice == EASY:
            UIElement(440, 130, "Easy").draw(self.screen, 30)
            self.draw_high_score("High Score: %.3f" % (self.high_score_easy if self.high_score_easy > 0 else 0))
        elif self.game_choice == MEDIUM:
            UIElement(440, 130, "Medium").draw(self.screen, 30)
            self.draw_high_score("High Score: %.3f" % (self.high_score_medium if self.high_score_medium > 0 else 0))
        elif self.game_choice == HARD:
            UIElement(440, 130, "Hard").draw(self.screen, 30)
            self.draw_high_score("High Score: %.3f" % (self.high_score_hard if self.high_score_hard > 0 else 0))

        self.draw_timer("%.3f" % self.elapsed_time)
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                quit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][
                                                                                               col + 1], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][
                                                                                               col - 1], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][
                                                                                               col], \
                                                                                           self.tiles_grid[row][col]

                            elif tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][
                                                                                               col], \
                                                                                           self.tiles_grid[row][col]
                            self.draw_tiles()
                            self.moves += 1

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "EASY":
                            self.game_choice = EASY
                            self.game_size = 3
                            self.new()
                        elif button.text == "MEDIUM":
                            self.game_choice = MEDIUM
                            self.game_size = 4
                            self.new()
                        elif button.text == "HARD":
                            self.game_choice = HARD
                            self.game_size = 5
                            self.new()
                        if button.text == "SHUFFLE":
                            self.shuffle_time = 0
                            self.start_shuffle = True
                        if button.text == "RESET":
                            self.new()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_shuffle = not self.start_shuffle

    def show_start_screen(self):
        self.game_choice = EASY
        self.game_size = 3

    def show_go_screen(self):
        pass



# create the game object
game = Game()
game.show_start_screen()
while True:
    game.new()
    game.run()
    game.show_go_screen()
