class Scene:
    def __init__(self, name, id=-1):
        self.name = name
        self.id = id
    
    def setId(self, id) :
        self.id = id
    
    def Update(self, camera, dt):
        pass

    def Draw(self, camera, screen):
        pass

    def start(self) :
        self.__init__(self.name, self.id)

    def dispose(self) :
        pass