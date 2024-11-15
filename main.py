import sys
import pygame
import pygame_menu
import pygame_menu.events
import pygame_menu.themes


pygame.init()
screen = pygame.display.set_mode((1152, 648))
clock = pygame.time.Clock() 
running = True

coords = [screen.get_width() / 2, screen.get_height() / 2]

class Base:
    def __init__(self, health, damage):
        self.health = health
        self.damage = damage
        self.attack_cooldown = 30
    def hit(self, damage):
        self.health -= damage
    def attack(self, target):
        target.hit(self.damage)
        self.attack_cooldown = 30

class Player(Base):
    pass
class NPC(Base):
    def dead(self):
        if self.health <= 0:
            return True
    pass

player = Player(10,1)
enemy = NPC(10,1)

def play(running, player, enemy):
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        delta_time = clock.tick(60) / 1000  # Limit FPS to 60, count delta time in milliseconds (hence the divide by 1000)
        screen.fill("black")

        pygame.draw.circle(screen, (255, 255, 255), coords, 10)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LCTRL]:
            if keys[pygame.K_w]:
                coords[1] -= 225 * delta_time
            if keys[pygame.K_s]:
                coords[1] += 225 * delta_time
            if keys[pygame.K_a]:
                coords[0] -= 225 * delta_time
            if keys[pygame.K_d]:
                coords[0] += 225 * delta_time
        
        else:
            if keys[pygame.K_w]:
                coords[1] -= 150 * delta_time
            if keys[pygame.K_s]:
                coords[1] += 150 * delta_time
            if keys[pygame.K_a]:
                coords[0] -= 150 * delta_time
            if keys[pygame.K_d]:
                coords[0] += 150 * delta_time


        if keys[pygame.K_f]:
            if player.attack_cooldown == 0:
                if "enemy" in locals():
                    player.attack(enemy)
                    print(enemy.health)
                    if enemy.dead():
                        del enemy
                else:
                    print("Enemy is dead")
        if player.attack_cooldown > 0:
            player.attack_cooldown -= 1



        pygame.display.update()

menu = pygame_menu.Menu("Welcome", screen.get_width(), screen.get_height(), theme=pygame_menu.themes.THEME_DARK)
menu.add.button("Play", play, running, player, enemy)
menu.add.button("Quit", pygame_menu.events.EXIT)

menu.mainloop(screen)