import pygame

from Mng.GameMng import GameMng
from Mng.MenuMng import MenuMng
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

# 카메라 객체 초기화
camera = Camera(screen.get_width(), screen.get_height())
# 입력 이벤트 감지 객체 초기화
input = InputMng(camera)

# 이미지 리소스 객체 초기화
imageProvider = ImageProvider()

# 이미지 리소스 불러오기
imageProvider.loadImage()

# 상태기기 초기화
# 화면의 상태를 관리
# 메뉴창, 인게임창, 결과창 등
# 스페이스바로 화면 전환 가능
# 메뉴에서 인게임으로 전환하는 예시
# sceneManager = SceneState([MenuMng(imageProvider=imageProvider), GameMng(imageProvider=imageProvider)])
# 단일
# sceneManager = SceneState([GameMng(imageProvider=imageProvider)])
sceneManager = SceneState([MenuMng(imageProvider=imageProvider), GameMng(imageProvider=imageProvider)])

while running:
    # 이벤트 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input.UpdateEvent(event)
        
    input.Update()
    
    # 씬 변경 테스트를 위해서 호출
    sceneManager.sceneChanger(input)

    sceneManager.getCurrentScene().Update(input, camera, dt)
    sceneManager.getCurrentScene().Draw(camera, screen)

    pygame.display.flip()

    # 프레임에 따라 움직이는 속도를 다르게 해야
    # 움직임이 튀지 않고 일정할 수 있다
    # 이때 필요한 것이 deltaTimes
    dt = clock.tick(60) / 1000
    
    # 이벤트 초기화
    input.lateUpdate()

pygame.quit()