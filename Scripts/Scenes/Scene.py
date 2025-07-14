# 화면 정보를 가지고 있는 상위 객체 추상화
# 상속하여 사용
class Scene:
    def __init__(self, name, id=-1):
        self.name = name
        self.id = id
    
    def setId(self, id) :
        self.id = id

    def getName(self) :
        return self.name
    
    def Update(self, camera, dt):
        pass

    def Draw(self, camera, screen):
        pass

    def start(self) :
        self.__init__(self.name, self.id)

    def dispose(self) :
        pass