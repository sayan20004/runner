#Libreries
import pygame
from sys import exit
from random import randint

#Diplaying score
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = Font_style.render(f'Score : {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

#Obstacles movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300: screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)
            
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100 ]
        return obstacle_list
    else:
        return []

#Collision Function 
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

#Player animation
def player_animation():
    global player_surface,player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]

#Variables and Settings
pygame.init()

#Game window
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Pixel Runner')
game_icon = pygame.image.load('graphics/player/player_stand.png')
pygame.display.set_icon(game_icon)
clock = pygame.time.Clock()
start_time = 0
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
Font_style = pygame.font.Font('font/Pixeltype.ttf',40)
game_acive = False
score = 0

#obstacle
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

#player surface
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surface = player_walk[player_index ]
player_rect = player_surface.get_rect(midbottom = (60,300))
player_gravity = 0

#game intro
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
stand_rect = player_stand.get_rect(center = (400,200))

game_name = Font_style.render('Pixel Runner',False,(111,196,169))
game_game_rect = game_name.get_rect(midtop = (410,100))

game_message =  Font_style.render('Press spacebar to run', False,(111,196,169))
game_message_rect = game_message.get_rect(midtop =(410,300))

#time 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

 
#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_acive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_acive = True
            start_time = int(pygame.time.get_ticks() / 1000) 
        if event.type == obstacle_timer and game_acive:
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))


    if game_acive:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))

        #player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface,player_rect)

        #obstacle
        obstacle_movement(obstacle_rect_list)
        score = display_score()

        #collision
        game_acive = collisions(player_rect,obstacle_rect_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = Font_style.render(f'Your Score : {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center= (400,330))
        screen.blit(game_name,game_game_rect)
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)