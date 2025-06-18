class Event:
    def __init__(self, description, font, effect_type=None, value=0):
        self.description = description
        self.text_surface = font.render(description, True, (255, 255, 255))
        self.effect_type = effect_type
        self.value = value

        self.rect = None  # 카드 위치를 저장할 Rect
        self.applied = False  # 이미 적용됐는지 여부

    # 클릭 시 필요한 이벤트 발생
    def apply(self, hero):
        if self.effect_type == "AP":
            hero.AP = min(hero.ApLimit, hero.AP + self.value)
            hero.UI.setAp(hero.AP / hero.ApLimit)
        elif self.effect_type == "Item":
            hero.bag.addItem(self.value["id"], self.value["item"], 1)
        elif self.effect_type == "Craft":
            for id in self.value["use"]:
                hero.bag.addItem(id, None, -1)
            hero.bag.addItem(self.value["id"], self.value["item"], 1)