class Node:
    def __init__(self, position=None, parent=None):
        self.position = position
        self.parent = parent
        self.g_score = 0
        self.h_score = 0
        self.f_score = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f_score < other.f_score

    def __repr__(self):
        return f"Node(position={self.position})"
    
    def __hash__(self):
        return hash(self.position)  # position을 기반으로 해시값 생성