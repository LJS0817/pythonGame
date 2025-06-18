import heapq
from Util.Node import Node

class PathProvider :
    def __init__(self):
        # 미리 생성
        self.open_list = []
        self.closed_set = set()

    def get_neighbors(self, map, pos):
        x = int(pos[0])
        y = int(pos[1])
        neighbors = []
        # [(-1, -1), (0, -1), (1, -1),
        #  (-1,  0),          (1,  0),
        #  (-1,  1), (0,  1), (1,  1)]  # 이동 가능한 범위
        # 육각형 그리드 특성으로 인해서 일부 인덱스 제외
        skipYIndex = 1 if x % 2 == 0 else -1

        for i in range(-1, 2, 1) :
            for j in range(-1, 2, 1) :
                # 육각형 그리드 특성으로 인해서 일부 인덱스 제외
                if (i == 0 and j == 0) or (i == skipYIndex and j != 0): continue
                new_x, new_y = x + j, y + i
                # -1은 이동 불가 공간
                if 0 <= new_y < len(map) and 0 <= new_x < len(map[0]) and map[new_y][new_x].getTileType() > -1: 
                    neighbors.append((new_x, new_y))

        return neighbors
    
    def heuristic(self, a, b):
        # 맨하탄 거리
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # 유클리드 거리
        # return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    def a_star(self, map, start, end):
        start_node = Node((start.x, start.y), None)
        end_node = Node((end.x, end.y), None)

        self.open_list.clear()
        self.open_list.append(start_node)
        self.closed_set.clear()

        while self.open_list:
            current_node = heapq.heappop(self.open_list)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # 역순으로 된 경로를 뒤집어서 반환

            self.closed_set.add(current_node)

            # 인접 노드 탐색
            neighbors = self.get_neighbors(map, current_node.position)

            for neighbor_pos in neighbors:
                neighbor = Node(neighbor_pos, current_node)

                if neighbor in self.closed_set:
                    continue

                neighbor.g_score = current_node.g_score + 1  # 이동 비용은 1이라고 가정
                neighbor.h_score = self.heuristic(neighbor.position, end_node.position)
                neighbor.f_score = neighbor.g_score + neighbor.h_score

                if neighbor not in self.open_list or neighbor.g_score < [node for node in self.open_list if node == neighbor][0].g_score:
                    heapq.heappush(self.open_list, neighbor)

        return None  # 경로를 찾지 못한 경우