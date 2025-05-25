  # Example file showing a circle moving on screen
import pygame

from Mng.GameMng import GameMng
from Mng.InputMng import InputMng

from Mng.Camera import Camera

from Scenes.SceneState import SceneState

from Provider.ImageProvider import ImageProvider

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 600))
clock = pygame.time.Clock()
running = True
dt = 0

camera = Camera(screen.get_width(), screen.get_height())
input = InputMng(camera)

imageProvider = ImageProvider()

imageProvider.loadImage()

sceneManager = SceneState([GameMng(imageProvider=imageProvider)])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input.UpdateEvent(event)
        
    input.Update()
    sceneManager.getCurrentScene().Update(input, camera, dt)
    sceneManager.getCurrentScene().Draw(camera, screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000
    
    input.lateUpdate()

pygame.quit()