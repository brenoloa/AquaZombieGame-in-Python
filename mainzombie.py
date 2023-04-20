import pygame
from pygame.locals import *
import time
import random
JANELA_LARGURA = 800
JANELA_ALTURA = 800
SPEED = 10
ZOMBIE_X = 250
ZOMBIE_Y = 210
GAME_SPEED = 10
GROUND_LARGURA = 2 * JANELA_LARGURA
GROUND_ALTURA = 300
PIPE_LARGURA = 80
PIPE_ALTURA = 500
PIPE_GAP = 350
GRAVITY = 1
SCORE = 0
class Zombie(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images =[pygame.image.load('zombie1.png').convert_alpha(),
                      pygame.image.load('zombie2.png').convert_alpha(),
                      pygame.image.load('zombie3.png').convert_alpha(),
                      pygame.image.load('zombie4.png').convert_alpha(),
                      pygame.image.load('zombie5.png').convert_alpha(),
                      pygame.image.load('zombie6.png').convert_alpha(),
                      pygame.image.load('zombie7.png').convert_alpha(),
                      pygame.image.load('zombie8.png').convert_alpha()]

        self.speed = SPEED #velocidade do zombie
        self.current_image = 0 #imagem atual
        self.image = pygame.image.load('zombie1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = ZOMBIE_X
        self.rect[1] = ZOMBIE_Y

    def update(self):
        self.current_image = (self.current_image + 1) % 7
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        #update de altura
        self.rect[1] += self.speed

    def bumb(self):
        self.speed = - SPEED



class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_LARGURA, PIPE_ALTURA))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = JANELA_ALTURA - ysize

        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_LARGURA, GROUND_ALTURA))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = JANELA_ALTURA - GROUND_ALTURA

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2]) #verifica se ochao esta fora da tela.

def get_random_pipes(xpos):
    size = random.randint(100, 500)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, JANELA_ALTURA - size - PIPE_GAP)
    return (pipe, pipe_inverted)

def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    text_rect = texto_formatado.get_rect(topleft=(310, 420))
    screen.blit(texto_formatado, text_rect)

def exibe_mensagem_novo(msg, tamanho, cor):
    fonte = pygame.font.SysFont('comicsansms', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    text_rect = texto_formatado.get_rect(topleft=(250 , 20))
    screen.blit(texto_formatado, text_rect)
# -=-=-=-= INICIO DA JANELA -=-=-=-=-=-
pygame.init()
screen = pygame.display.set_mode((JANELA_LARGURA, JANELA_ALTURA))
pygame.display.set_caption('AquaZombie')
GAME_OVER = pygame.image.load('gameover.png').convert_alpha()
# -=-=-=-=-=-=-=-= -=-=-= -=-=-= -=-= -=-=
BACKGROUND = pygame.image.load('background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (JANELA_LARGURA, JANELA_ALTURA))
# -=-=-
zombie_group = pygame.sprite.Group()
zombie = Zombie()
zombie_group.add(zombie)
#-=-=-=-=-=
passed_pipes = pygame.sprite.Group()
#-=-=-=-=
font = pygame.font.Font('04B_19__.TTF', 46)
text = font.render("Score: " + str(SCORE), 1, (255, 255, 255))
screen.blit(text, (10, 10))
#-=-=-=

#-=-=-=-=-=
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_LARGURA * i)
    ground_group.add(ground)

    pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(JANELA_LARGURA * i + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
# habilitador de fps
game_over = False
clock = pygame.time.Clock()
while True:
    clock.tick(30) #fps
    exibe_mensagem_novo("github.com/brenoloa", 30, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not game_over:
                    zombie.bumb()
                else:
                    SCORE = 0
                    zombie_group.empty()
                    zombie = Zombie()
                    zombie_group.add(zombie)

                    pipe_group.empty()
                    for i in range(2):
                        pipes = get_random_pipes(JANELA_LARGURA * i + 600)
                        pipe_group.add(pipes[0])
                        pipe_group.add(pipes[1])

                    game_over = False

    if not game_over:
        screen.blit(BACKGROUND, (0, -50))
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_LARGURA - 60)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(JANELA_LARGURA * 2)

            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        zombie_group.update()
        pipe_group.update()
        ground_group.update()
        passed_pipes.update()

        zombie_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)
        text = font.render("" + str(SCORE), 1, (255, 255, 255))
        screen.blit(text, (390, 100))

        # Verifica colisões
        if pygame.sprite.groupcollide(zombie_group, ground_group, False, False, pygame.sprite.collide_mask) or\
            pygame.sprite.groupcollide(zombie_group, pipe_group, False, False, pygame.sprite.collide_mask):
            game_over = True

        # Mostra a mensagem de Game Over
        if game_over:
            screen.blit(GAME_OVER, (JANELA_LARGURA / 2 - GAME_OVER.get_width() / 2, JANELA_ALTURA / 2 - GAME_OVER.get_height() / 2))

            exibe_mensagem("Pressione ESPAÇO", 20, (255, 255, 255))
            exibe_mensagem("Pressione ESPAÇO", 20, (255, 255, 255))

    for pipe in pipe_group:
        if pipe.rect.right < zombie.rect.left and pipe not in passed_pipes:
            SCORE += 1
            passed_pipes.add(pipe)


    pygame.display.update()