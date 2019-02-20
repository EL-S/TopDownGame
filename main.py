import pygame
from random import randint
import math
import time

tiles = {}

tiles_data = {}

player = {}

player['pos'] = [0,0]

pygame.init()
info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
screen_width,screen_height = info.current_w,info.current_h
print(screen_width,screen_height)

grid_size = 40 #automate the process of picking this number so it perfectly fits

grid_height = round(screen_height/grid_size)
grid_width = round(screen_width/grid_size)

print(grid_height,grid_width)

max_val = 10

for x in range(grid_width): #bad but not that bad
    for y in range(grid_height):
        value = randint(0,max_val)
        if value == max_val:
            tiles[(x,y)] = 1 #1 is water
        else:
            tiles[(x,y)] = 0 #0 is grass, nothing would be faster though

width = grid_size*grid_width
height = grid_size*grid_height

surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def draw_screen():
    offset_x = player['pos'][0]
    offset_y = player['pos'][1]
    
    surface.fill((255,255,255))

    draw_tiles() 

    draw_player()

    pygame.display.update()

def draw_tiles():
    global tiles, player

    offset_x = player['pos'][0]
    offset_y = player['pos'][1]
    
    for x in range(grid_width):
        for y in range(grid_height):
            cell_x = x+offset_x
            cell_y = y+offset_y
            try:
                value = tiles[(cell_x,cell_y)]
            except:
                value = randint(0,max_val)
                if value == max_val:
                    tiles[(cell_x,cell_y)] = 1 #1 is water
                else:
                    tiles[(cell_x,cell_y)] = 0 #0 is grass, nothing would be faster though
                value = tiles[(cell_x,cell_y)]
            if value == 1:
                colour = (0,0,255)
            elif value == 0:
                colour = (0,255,0)
            else:
                colour = (0,0,0)
            fill_cell(x+player['pos'][0],y+player['pos'][1],colour)

def fill_cell(x,y,colour):
    global grid_size, grid_width, grid_height
    offset_x = x-player['pos'][0]
    offset_y = y-player['pos'][1]
    x_pixel = offset_x*grid_size
    y_pixel = offset_y*grid_size
    pygame.draw.rect(surface, colour, pygame.Rect(x_pixel, y_pixel, grid_size, grid_size))

def draw_player():
    global moves, player, food, history, grid_width, grid_height, food_move_gain
    
    cell_x = int(grid_width/2)+player['pos'][0]
    cell_y = int(grid_height/2)+player['pos'][1]

    colour = (255,0,0)
    
    fill_cell(cell_x,cell_y,colour)

def key_check():
    global player, running
    events = pygame.event.get()
    #listen for input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        return
    if keys[pygame.K_w]:
        player['pos'][1] -= 1
        draw_screen()
    if keys[pygame.K_a]:
        player['pos'][0] -= 1
        draw_screen()
    if keys[pygame.K_s]:
        player['pos'][1] += 1
        draw_screen()
    if keys[pygame.K_d]:
        player['pos'][0] += 1
        draw_screen()

running = True


draw_screen()
while running:
    key_check()

pygame.quit()
