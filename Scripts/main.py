# Example file showing a circle moving on screen
import pygame

from Mng.GameMng import GameMng
from Mng.InputMng import InputMng

from Mng.Camera import Camera

from Scenes.SceneState import SceneState

from Provider.ImageProvider import ImageProvider

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True
dt = 0

camera = Camera(screen.get_width(), screen.get_height())
input = InputMng(camera)

imageProvider = ImageProvider()

imageProvider.loadImage()

sceneManager = SceneState([GameMng(imageProvider=imageProvider)])

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if event.type == pygame.KEYDOWN :
        #     print("KEYDOWN")

    # camera.setPosition(pygame.mouse.get_pos())
    input.Update()
    sceneManager.getCurrentScene().Update(input, camera, dt)
    sceneManager.getCurrentScene().Draw(camera, screen)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()