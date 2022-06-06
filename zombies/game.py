from logging import NullHandler
import pygame
from .player import Player
from .zombie import Zombie
pygame.init()

class GameInformation:
    def __init__(self, score, player, zombies):
        self.score = score
        self.player_x = player.coordinates[0]
        self.player_y = player.coordinates[1]

        zombie_locations = []
        for zombie in zombies:
            zombie_locations.append(zombie.coordinates)
        self.zombies_locations = zombie_locations

class AvailableLocations:
    def __init__(self, score, available_moves):
        self.score = score
        self.available_moves = available_moves


class Game:
    SCORE_FONT = pygame.font.SysFont("arial", 50)
    GAME_WIDTH = 1000
    GAME_HEIGHT = 700
    RADIUS = 10
    SPACE_SIZE = 10
    TOTAL_ZOMBIES = 24
    ZOMBIE_SPEED = 3

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.window = window

        self.score = 0
        self.direction = 2
        self.player = Player(self.GAME_WIDTH, self.GAME_HEIGHT, self.RADIUS)
        zombies = []
        for i in range(self.TOTAL_ZOMBIES):
            zombie = Zombie(0, self.player.coordinates, self.GAME_WIDTH, self.GAME_HEIGHT, self.RADIUS, self.SPACE_SIZE)
            zombies.append(zombie)
        self.zombies = zombies 

    def draw_score(self):
        score_text = self.SCORE_FONT.render(f"{self.score}", 1, (255,0,0))
        self.window.blit(score_text, (self.window_width // 2 - score_text.get_width()//2, 10))

    def draw(self, draw_score=True, draw_textures=False):
        self.window.fill((0,0,0))

        if draw_score:
            self.draw_score()

        for zombie in self.zombies:
            zombie.draw(self.window, draw_textures)

        self.player.draw(self.window, draw_textures)

    def kill_zombies(self):
        zombiesKilled = 0
        for zombie in self.zombies:
            if(zombie.timeBorn + zombie.ttl < self.score):
                zombiesKilled += 1
                self.zombies.remove(zombie)
                del zombie

        for i in range(zombiesKilled):
            z = Zombie(self.score, self.player.coordinates, self.GAME_WIDTH, self.GAME_HEIGHT, self.RADIUS, self.SPACE_SIZE)
            self.zombies.append(z)

    def in_bounds_x(self, x):
        if(x < 0 or x > self.GAME_WIDTH):
            return False
        else:
            return True

    def in_bounds_y(self, y):
        if(y < 0 or y > self.GAME_HEIGHT):
            return False
        else:
            return True

    def next_turn(self):
        x,y = self.player.coordinates
        
        if self.check_collisions():
            gameinfo = {
                "alive": False,
                "info": AvailableLocations(self.score, self.available_moves())
            }
            return gameinfo
        else:
            if self.direction == 1 and self.in_bounds_y(y-self.SPACE_SIZE):
                y-=self.SPACE_SIZE
            elif self.direction == 2 and self.in_bounds_y(y+self.SPACE_SIZE):
                y+=self.SPACE_SIZE       
            elif self.direction == 3 and self.in_bounds_x(x-self.SPACE_SIZE):
                x-=self.SPACE_SIZE  
            elif self.direction == 4 and self.in_bounds_x(x+self.SPACE_SIZE):
                x+=self.SPACE_SIZE  

            #Player not dead, add score
            self.player.move(x,y)
            self.score += 1

            self.kill_zombies()
            if(self.score % self.ZOMBIE_SPEED == 0):
                self.move_zombies()
            
            #Return Game Information
            available = self.available_moves()
            gameinfo = {
                "alive": True,
                "info": AvailableLocations(self.score, available)
            }
            return gameinfo

    def move_zombies(self):
        x,y = self.player.coordinates
        
        for zombie in self.zombies:
            zx, zy = zombie.coordinates
            deltaX = x - zx
            deltaY = y - zy

            if (deltaX < 0 and deltaY > 0):
                #left/down
                if (not self.zombie_is_in_location(zx - self.SPACE_SIZE, zy + self.SPACE_SIZE)) and zy + self.SPACE_SIZE <= self.GAME_HEIGHT and zx - self.SPACE_SIZE >= 0:
                    zombie.coordinates = [zx - self.SPACE_SIZE, zy + self.SPACE_SIZE]
            elif(deltaX < 0 and deltaY == 0):
                #left
                if not self.zombie_is_in_location(zx - self.SPACE_SIZE, zy) and zx - self.SPACE_SIZE >= 0:
                    zombie.coordinates = [zx - self.SPACE_SIZE , zy]
            elif (deltaX < 0 and deltaY < 0):
                #left/up
                if not self.zombie_is_in_location(zx - self.SPACE_SIZE, zy - self.SPACE_SIZE) and zy - self.SPACE_SIZE >= 0 and zx - self.SPACE_SIZE >= 0:
                    zombie.coordinates = [zx - self.SPACE_SIZE, zy - self.SPACE_SIZE]
            elif(deltaX == 0 and deltaY < 0):
                #Up
                if not self.zombie_is_in_location(zx, zy - self.SPACE_SIZE) and zy - self.SPACE_SIZE >= 0:
                    zombie.coordinates = [zx , zy - self.SPACE_SIZE]
            elif (deltaX > 0 and deltaY < 0):
                #right/up
                if not self.zombie_is_in_location(zx + self.SPACE_SIZE, zy - self.SPACE_SIZE) and zy - self.SPACE_SIZE >= 0 and zx + self.SPACE_SIZE <= self.GAME_WIDTH:
                    zombie.coordinates = [zx + self.SPACE_SIZE, zy - self.SPACE_SIZE]
            elif(deltaX > 0 and deltaY == 0):
                #right
                if not self.zombie_is_in_location(zx + self.SPACE_SIZE, zy) and zx + self.SPACE_SIZE <= self.GAME_WIDTH:
                    zombie.coordinates = [zx + self.SPACE_SIZE, zy]
            elif (deltaX > 0 and deltaY > 0):
                #right/down
                if not self.zombie_is_in_location(zx + self.SPACE_SIZE, zy + self.SPACE_SIZE) and zy + self.SPACE_SIZE <= self.GAME_HEIGHT and zx + self.SPACE_SIZE <= self.GAME_WIDTH:
                    zombie.coordinates = [zx + self.SPACE_SIZE, zy + self.SPACE_SIZE]
            elif(deltaX == 0 and deltaY > 0):
                #down
                if not self.zombie_is_in_location(zx, zy + self.SPACE_SIZE) and zy + self.SPACE_SIZE <= self.GAME_HEIGHT:
                    zombie.coordinates = [zx , zy + self.SPACE_SIZE]

    def zombie_is_in_location(self, x, y):
        for zombie in self.zombies:
            if(zombie.coordinates[0] == x and zombie.coordinates[1] == y):
                return True
        return False

    def change_direction(self, new_direction):
        self.direction = new_direction

    def check_collisions(self):
        x,y = self.player.coordinates
        for zombie in self.zombies:
            if(x == zombie.coordinates[0] and y == zombie.coordinates[1]):
                return True

        return False

    def reset(self):
        self.score = 0
        self.direction = 1
        self.player = 0
        self.zombies = []    

    def available_moves(self):
        #[0  1         2      3           4     5          6     7      ]
        #[UP,UP-RIGHT, RIGHT, DOWN-RIGHT, DOWN, DOWN-LEFT, LEFT, LEFT-UP]
        x,y = self.player.coordinates
        space = self.SPACE_SIZE
        available = [1,1,1,1,1,1,1,1]
        coordinates = [[x,y-space],[x+space,y-space],[x+space,y],[x+space,y+space],[x,y+space],[x-space,y+space],[x-space,y],[x-space,y-space]]
        
        #check edges
        if(x == 0):
            available[1] = 0
            available[2] = 0
            available[3] = 0
        elif(x == self.GAME_WIDTH):
            available[5] = 0
            available[6] = 0
            available[7] = 0
        if(y == 0):
            available[7] = 0
            available[0] = 0
            available[1] = 0
        elif(y == self.GAME_HEIGHT):
            available[3] = 0
            available[4] = 0
            available[5] = 0

        #check if Zombies are in remaining locations
        for i in range(len(available)):
            if(available[i] == 1):
                px, py = coordinates[i]
                for zombie in self.zombies:
                    zx, zy = zombie.coordinates
                    if(zx == px and zy == py):
                        available[i] = 0
                        break
        
        return available


