import random
import pygame
import os

class Zombie:
    
    def __init__(self, time, player, width, height, radius, space_size):
        #Randomly generate coordinates 
        player_x, player_y = player
        x = random.randint(0,height/space_size-1)*space_size
        y = random.randint(0,width/space_size-1)*space_size
        while((x<(player_x + 250) and x>(player_x - 250)) and (y<player_y + 250 and y>player_y - 250)):
            x = random.randint(0,width/space_size-1)*space_size
            y = random.randint(0,height/space_size-1)*space_size
        
        self.coordinates = [x,y]
        self.timeBorn = time
        self.ttl = random.randint(0,200) + 200
        self.radius = radius

        self.texture = pygame.image.load(os.path.join('zombies/img', "zombie.png"))
        self.texture = pygame.transform.scale(self.texture, (self.radius*2, self.radius*2))

    def draw(self, win, texture):
        if(texture):
            rect = pygame.Rect(self.coordinates[0]-(self.radius), self.coordinates[1]-(self.radius), 10, 10)
            win.blit(self.texture, rect)
        else:
            pygame.draw.circle(win, (255, 0, 0), (self.coordinates[0], self.coordinates[1]), self.radius)
