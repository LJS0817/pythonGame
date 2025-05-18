class SceneState:
    def __init__(self, sceneList, startIndex=0):
        self.list = sceneList

        for i in range(len(sceneList)):
            self.list[i].setId(i)

        self.curIndex = startIndex
        self.getCurrentScene().start()
    
    def changeScene(self, idx) :
        self.getCurrentScene().dispose()
        self.curIndex = idx
        self.getCurrentScene().start()

    def getCurrentScene(self) :
        return self.list[self.curIndex]