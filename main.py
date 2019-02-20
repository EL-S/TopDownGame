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

max_val = 100

def get_surrounding_cells(x,y):
    total = 0
    for i in range(-1,2):
        for ii in range(-1,2):
            try:
                value = tiles[(x+i,y+ii)]
                if value == 1 or value == 4: #if water nearby
                    total += 1
            except:
                pass

    return total

def gen_tile(x,y):
    total = get_surrounding_cells(x,y)
    water_chance = total*1200
    if water_chance == 0:
        water_chance = 1
    value = randint(0,10000)
    if value < water_chance:
        randvalue = randint(0,1)
        if randvalue == 0:
            tiles[(x,y)] = 1 #1 is water
        else:
            tiles[(x,y)] = 4 #4 is light water
        for i in range(-1,2):
            for ii in range(-1,2):
                try:
                    tiles[(x+i,y+ii)]
                except: #if a surrounding tile doesn't exist
                    if value < water_chance:
                        randvalue = randint(0,1)
                        if randvalue == 0:
                            tiles[(x+i,y+ii)] = 1 #1 is water
                        else:
                            tiles[(x+i,y+ii)] = 4 #4 is light water   
    else:
        #land tile
        flowerchance = 100
        light_grass_chance = 300
        value = randint(0,1000)
        if value < flowerchance:
            tiles[(x,y)] = 3 #flower
            tiles_data[(x,y)] = {}
            tiles_data[(x,y)]['colour'] = (randint(0,255),randint(0,255),randint(0,255))
            randvalue = randint(0,1)
            if randvalue == 0:
                background_tile = 0
            else:
                background_tile = 2
            tiles_data[(x,y)]['background_tile'] = background_tile
            tiles_data[(x,y)]['petal_colour'] = (randint(0,255),randint(0,255),randint(0,255))
            #flower background and colour
        elif value < light_grass_chance:
            tiles[(x,y)] = 2 #light grass
        else:
            tiles[(x,y)] = 0 #0 is grass, nothing would be faster though

for x in range(grid_width): #bad but not that bad
    for y in range(grid_height):
        gen_tile(x,y)


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

    colours = {"grass":(0,255,0),
               "light_grass":(127,255,0),
               "water":(0,0,255),
               "light_water":(0,25,255)}
    
    for x in range(grid_width):
        for y in range(grid_height):
            cell_x = x+offset_x
            cell_y = y+offset_y
            fill_x = x+player['pos'][0]
            fill_y = y+player['pos'][1]
            try:
                value = tiles[(cell_x,cell_y)]
            except:
                gen_tile(cell_x,cell_y)
                value = tiles[(cell_x,cell_y)]
            if value == 0:
                colour = colours['grass']
            elif value == 1:
                colour = colours['water']
            elif value == 2:
                colour =  colours['light_grass']
            elif value == 3: #flower
                colour1 = tiles_data[(cell_x,cell_y)]['colour']
                colour2 = tiles_data[(cell_x,cell_y)]['petal_colour']
                background_tile = tiles_data[(cell_x,cell_y)]['background_tile']
                if background_tile == 0:
                    colour3 = colours['grass']
                if background_tile == 2:
                    colour3 = colours['light_grass']
                fill_cell(fill_x,fill_y,colour3) #add grass
                fill_cell_thirds(fill_x,fill_y,colour1,[1,1]) #center bud
                fill_cell_thirds(fill_x,fill_y,colour2,[1,0]) #petal top
                fill_cell_thirds(fill_x,fill_y,colour2,[1,2]) #petal bottom
                fill_cell_thirds(fill_x,fill_y,colour2,[0,1]) #petal left
                fill_cell_thirds(fill_x,fill_y,colour2,[2,1]) #petal right
            elif value == 4:
                colour =  colours['light_water']
            else:
                colour = (0,0,0) #error
            if value != 3:
                fill_cell(fill_x,fill_y,colour)

def fill_cell_thirds(x,y,colour,pos):
    global grid_size, grid_width, grid_height
    #0,0|1,0|2,0
    #0,1|1,1|2,1
    #0,2|1,2|2,2
    offset_x = x-player['pos'][0]
    offset_y = y-player['pos'][1]
    small_size = round(grid_size/3)
    mini_offset_x = pos[0]*small_size
    mini_offset_y = pos[1]*small_size
    x_pixel = (offset_x*grid_size)+mini_offset_x
    y_pixel = (offset_y*grid_size)+mini_offset_y
    pygame.draw.rect(surface, colour, pygame.Rect(x_pixel, y_pixel, small_size, small_size))
                     
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

    colour = (139,69,19)
    
    fill_cell(cell_x,cell_y,colour)

def key_check(): #yuck
    global player, running
    events = pygame.event.get()
    #listen for input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        return
    if keys[pygame.K_w]:
        move('up')
    if keys[pygame.K_a]:
        move('left')
    if keys[pygame.K_s]:
        move('down')
    if keys[pygame.K_d]:
        move('right')

def move(direction):
    cell_x = int(grid_width/2)+player['pos'][0]
    cell_y = int(grid_height/2)+player['pos'][1]
    water_tiles = [1,4]
    if direction == 'up':
        if tiles[cell_x,cell_y-1] not in water_tiles:
            player['pos'][1] -= 1
    elif direction == 'down':
        if tiles[cell_x,cell_y+1] not in water_tiles:
            player['pos'][1] += 1
    elif direction == 'left':
        if tiles[cell_x-1,cell_y] not in water_tiles:
            player['pos'][0] -= 1
    elif direction == 'right':
        if tiles[cell_x+1,cell_y] not in water_tiles:
            player['pos'][0] += 1
    draw_screen()

running = True


draw_screen()
while running:
    key_check()

pygame.quit()
