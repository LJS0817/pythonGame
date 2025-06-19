from ..Unit import Unit
from Unit.UI.HeroUI import HeroUI
from Provider.EventProvider import EventProvider
from pygame.math import Vector2
from Unit.Inventory.Inventory import Inventory
from Unit.UI.FadeOutEffect import FadeEffect
import pygame
import random

class Hero(Unit):
    def __init__(self, center, imgPro, itemPro, uiMng) :
        super().__init__()
        # 이동 속도
        self.moveLimitTime = 0.4
        self.ApLimit = 10

        self.font = uiMng
        self.bag = Inventory(imgPro, self.font, self)
        self.UI = HeroUI(imgPro)

        self.itemProvider = itemPro
        self.eventProvider = EventProvider(uiMng, imgPro, itemPro)

        self.reset(center)

    # 씬 초기화용
    def reset(self, center) :
        self.position = center
        self.worldPosition = None
        self.prevPos = None
        self.path = None
        self.targetIndex = 0
        
        # 이동 속도
        self.moveTime = self.moveLimitTime

        self.AP = self.ApLimit + 1
        self.ap_effects = []

        self.debugItemIndex = 1

        self.bag.reset()
        self.itemProvider.reset()

    def Update(self, input, mapMng, dt):
        # 테스트용 키
        self.forText(input, mapMng)
        
        # 인벤토리 활성화/비활성화
        if input.isKeyDown(pygame.K_i) :
            self.showInventory()

        # 움직이기 위한 로직    
        self.Move(input, mapMng, dt)

        # 인벤토리 활성화 시 업데이트 수행
        self.bag.update(input)
        # AP에 변화가 있는 경우 이펙트 출력
        self.ap_effects = [fx for fx in self.ap_effects if fx.update(dt)]

    # 테스트 시 사용하는 키 모음
    def forText(self, input, mapMng) :
        # AP 충전
        if input.isKeyDown(pygame.K_q) :
            self.changeAP(self.ApLimit)
        # 아이템 랜덤 생성
        if input.isKeyDown(pygame.K_s) :
            rand = random.randrange(1, 9)
            self.bag.addItem(f"{rand}", self.itemProvider.getItem(f"{rand}"), 1)
        # 아이템 ID 순으로 생성
        if input.isKeyDown(pygame.K_a) :
            self.bag.addItem(f"{self.debugItemIndex}", self.itemProvider.getItem(f"{self.debugItemIndex}"), 1)
            self.debugItemIndex += 1
            if self.debugItemIndex > 8 :
                self.debugItemIndex = 1

    # A* 알고리즘으로 활성화면 경로를 따라 이동
    def FollowPath(self, dt) :
        if self.path == None : return
        self.moveTime += dt
        if self.moveTime >= self.moveLimitTime :
            self.moveTime = 0
            self.position = Vector2(self.path[self.targetIndex][0], self.path[self.targetIndex][1])
            self.targetIndex += 1
            if self.targetIndex >= len(self.path) :
                self.targetIndex = 0
                self.path = None

    # 패스 초기화
    def clearPath(self, mapMng) :
        if self.path != None :
            # 경로가 남아 있다면 타일을 이전 타일로 변경
            for i in range(self.targetIndex, len(self.path)) :
                p = Vector2(self.path[i][0], self.path[i][1])
                mapMng.setMapIndex(p, mapMng.getMapChangeIndex((p.x, p.y)))
            self.path = None

    # AP 변화
    def changeAP(self, cnt) :
        self.AP += cnt
        if self.AP > self.ApLimit :
            self.AP = self.ApLimit
        elif self.AP < 0 : 
            self.AP = 0
        self.UI.setAp(self.AP / self.ApLimit if self.AP > 0 else 0)

        text = self.font.getFont(24).render(f"{cnt} AP", True, (255, 255, 255))
        self.ap_effects.append(FadeEffect(text, self.worldPosition.copy())) 

    # 움직임 로직
    def Move(self, input, mapMng, dt) :
        # 인벤토리가 표시되고 있지 않으면
        if not self.bag.isShowing() :
            # 마우스 위치에 있는 타일을 강으로 변경
            if input.isKeyDown(pygame.K_z):
                if not mapMng.isSameTarget(input.getMousePosition()) :
                    mapMng.setMapIndex(mapMng.getHex(input.getMousePosition().x, input.getMousePosition().y), 2)
            # 마우스 우클릭으로 마우스 위치에 있는 타일을 삭제
            if input.isMouseDown(1):
                if not mapMng.isSameTarget(input.getMousePosition()) :
                    mapMng.setMapIndex(mapMng.getHex(input.getMousePosition().x, input.getMousePosition().y), -1)
            
            # 마우스 좌클릭 시
            if input.isMouseDown(0):
                # 이벤트 목록이 보이고 있다면
                if self.eventProvider.isShowing() :
                    # 마우스 출돌을 체크하고 충돌 시에 이벤트 발생 처리
                    self.eventProvider.handle_click(pygame.mouse.get_pos(), self)
                    # 현재 플레이어 위치를 클릭했다면
                elif (self.path == None or len(self.path) == 1) and mapMng.isSameTarget(input.getMousePosition()) : 
                    # Hero의 현재 위치 주변에 강 타일이 있는지 확인
                    is_near_river = mapMng.isTileTypeNearby(self.position, "River", radius=1)
                    # 이벤트 생성 및 표시
                    self.eventProvider.generateEvents(input.camera.getPosition(), self.bag, is_near_river)
                    # AP > 0 인 상태에서 플레이어 위치를 제외한 다른 타일을 클릭했다면
                elif self.path == None and not mapMng.isSameTarget(input.getMousePosition()) and self.AP > 0 :
                    # 남아있는 경로가 있다면 해당 경로를 정리
                    self.setTileNearestTile(mapMng)
                    # 경로 검색
                    self.path = mapMng.findPath(self.position, input.getMousePosition(), self.path)
                    self.targetIndex = 0
                    # 현재 위치에 플레이어 타일이 없다면
                if self.path != None and mapMng.getMapIndex(self.position) != 4:
                    mapMng.setMapIndex(self.position, 4)
            
            # 경로 추적
            self.FollowPath(dt)

        # 움직인 이후 이전의 타일을 바꾸기 위한 분기
        if(self.prevPos == None or self.prevPos != self.position) :
            if self.prevPos != None : 
                mapMng.setMapIndex(self.prevPos, mapMng.getMapChangeIndex((self.prevPos.x, self.prevPos.y)))
            mapMng.setMapIndexWithSplash(self.position, "Hero")
            self.worldPosition = mapMng.toWorldPosition(self.position)
            self.changeAP(-1)
            # AP가 0이라면 경로를 정리하고 현재 위치를 MapMng에도 저장
            if self.AP <= 0 :
                self.AP = 0
                self.setTileNearestTile(mapMng)
                mapMng.setTargetOutAp(self.position)
            self.prevPos = Vector2.copy(self.position)

        # 카메라 위치 이동
        input.camera.smoothMove(self.worldPosition)
    
    # 남아 있는 경로를 정리
    def setTileNearestTile(self, mapMng) :
        if self.path != None :
            if self.targetIndex < len(self.path) :
                pos = self.path[self.targetIndex]
                idx = mapMng.getMapChangeIndex(pos)
                pos = Vector2(pos[0], pos[1])
                print(idx, pos)
                if idx == 0 and mapMng.getMapIndex(pos) == 3:
                    mapMng.setMapIndex(pos, 1)
            self.clearPath(mapMng)

    # 인벤토리 활성화/비활성화
    def showInventory(self) :
        self.bag.showInventory()

    # 렌더링
    def Draw(self, camera, screen):
        for fx in list(self.ap_effects):
            fx.draw(screen, camera)
        self.eventProvider.draw(screen, camera.size)
        self.bag.drawItem(camera, screen)
        self.UI.Draw(camera, screen)
    
    def Clipping(self):
        pass