import math
from heapq import heappush, heappop # using priority queue for A*


class CyclingRouter:

    def __init__(self, locations: dict[str, list[float]], 
                 network: dict[str, list[str]], profiles: dict[str, float]):
        self.locations = locations
        self.network = network
        self.profiles = profiles
        self.scale_factor = 100 # 1 unit in map is 100 metres in reality


    def is_symmetric_network(self):
        for vertex, neighbours in self.network.items():
            for neighbour in neighbours:
                if neighbour not in self.network or vertex not in self.network[neighbour]:
                    print('The network is not symmetric between nodes', vertex, 'and', neighbour)
                    return False
        return True


    def correct_parameters(self, start: str, goal: str, profile: str) -> bool:
        if start not in self.locations or goal not in self.locations:
            print('Selected locality is not part of graph.')
            return False
        if profile not in self.profiles:
            print('Selected profile is in incorrect format. Use from {flat, hilly, mountain}.')
            return False
        return True

        
    def euclidean_distance(self, start: str | None, goal: str | None) -> float:
        if not start or not goal:
            return 0

        x1, y1, _ = self.locations[start]
        x2, y2, _ = self.locations[goal]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def edge_cost(self, node1: str, node2: str, profile: str) -> float:
        _, _, el_node1 = self.locations[node1]
        _, _, el_node2 = self.locations[node2]
        elevation = max(0, el_node2 - el_node1) # elevation between two nodes
        return self.euclidean_distance(node1, node2) + elevation * self.profiles[profile]


    def heuristic(self, start: str, goal: str, profile: str) -> float:
        _, _, el_start = self.locations[start]
        _, _, el_goal = self.locations[goal]
        elevation = max(0, el_goal - el_start) # minimal possible elevation gain
        return self.euclidean_distance(start, goal) + elevation * self.profiles[profile]


    def a_star(self, start: str, goal: str, profile: str) -> tuple[float, list[str], float]:

        if not self.correct_parameters(start, goal, profile):
            return 0.0, [], 0.0

        start_heuristic = self.heuristic(start, goal, profile)

        heap: list[tuple[float, str]] = [(start_heuristic, start)]
        predecessors: dict[str, str | None] = {start: None}
        visited: set[str] = set()
        cost_from_start: dict[str, float] = {start: 0}

        while heap: 

            _, current = heappop(heap)
            if current in visited:
                continue
            if current == goal:
                break

            visited.add(current)

            for neighbour in self.network[current]:
                new_cost = cost_from_start[current] + self.edge_cost(current, neighbour, profile)

                if neighbour not in cost_from_start or new_cost < cost_from_start[neighbour]:

                    cost_from_start[neighbour] = new_cost
                    val = new_cost + self.heuristic(neighbour, goal, profile)
                    predecessors[neighbour] = current

                    heappush(heap, (val, neighbour))

        if goal not in predecessors: # the goal is not reachable
            return 0.0, [], 0.0

        return self.reconstruct_path(goal, predecessors)


    def reconstruct_path(self, goal: str, predecessors: \
                         dict[str, str | None]) -> tuple[float, list[str], float]:
        distance: float = 0
        result: list[str] = []
        current: str = goal
        while current:
            distance += self.euclidean_distance(current, predecessors[current])
            result.append(current)
            current = predecessors[current]
        result.reverse()

        elevation = self.overall_elevation(result)
        return distance * self.scale_factor, result, elevation


    def overall_elevation(self, seq_nodes: list[str]) -> float:
        if len(seq_nodes) < 2:
            return 0
        result = 0
        for i in range(1, len(seq_nodes)):
            _, _, el_start = self.locations[seq_nodes[i - 1]]
            _, _, el_goal = self.locations[seq_nodes[i]]
            if el_goal > el_start:
                result += (el_goal - el_start)

        return result


class Rider():

    def __init__(self, weight: float, zone: int):
        self.weight = weight
        self.zone = zone

    def correct_parameters(self) -> bool:
        if self.zone not in {1, 2, 3, 4, 5}:
            print("Incorrect zone format: Use only number from 1 to 5.")
            return False
        if 150 < self.weight > 30:
            print("Minimum of weight limit is set at 30 kg a maximum is set at 150 kg")
            return False
        return True

    def calculate():
        pass
        # calculation of watts, average speed, ...



PROFILES = {
    "flat" : 0.5,
    "hilly" : 0.25,
    "mountain" : 0
}

LOCATIONS = { 
    "Prygl": [0, 0, 233],
    "Rozhledna Holedná": [0, 47, 309],
    "Wilsonov les": [55, 35, 255],
    "TechnoPark": [58 ,0, 260],
    "Semilasso": [75 ,2, 233],
    "Rouvy Office": [76, 32, 255],
    "Fi Muni": [81, 30, 220],
    "Tugendhat Villa": [97, 36, 217],
    "Koliště": [94, 47, 217],
    "Špilberk": [79, 53, 282],
    "Anthropos": [45, 60, 208],
    "Velodrom": [62, 70, 205],
    "Winning Group Arena": [83, 68, 201],
    "Hlavní nádraží": [95, 59, 206],
    "HANGAR Brno": [84, 97, 213],
    "Stránska skála": [160, 63, 310]
}

ROAD_NETWORK = {
    "Prygl": ["Wilsonov les"],
    "Rozhledna Holedná": ["Wilsonov les"],
    "Wilsonov les": ["Prygl", "Rouvy Office", "Anthropos", "Rozhledna Holedná"],
    "TechnoPark": ["Semilasso", "Rouvy Office"],
    "Semilasso": ["TechnoPark", "Rouvy Office", "Fi Muni"],
    "Rouvy Office": ["TechnoPark", "Semilasso", "Fi Muni", "Wilsonov les", "Špilberk", "Koliště"],
    "Fi Muni": ["Semilasso", "Rouvy Office", "Tugendhat Villa", "Koliště"],
    "Tugendhat Villa": ["Fi Muni", "Koliště"],
    "Koliště": ["Fi Muni", "Tugendhat Villa", "Hlavní nádraží", "Rouvy Office", "Špilberk"],
    "Špilberk": ["Rouvy Office", "Velodrom", "Winning Group Arena", "Koliště", "Anthropos", "Hlavní nádraží"],
    "Anthropos": ["Wilsonov les", "Velodrom", "Špilberk"],
    "Velodrom": ["Anthropos", "Winning Group Arena", "Špilberk"],
    "Winning Group Arena": ["Velodrom", "Špilberk", "Hlavní nádraží", "HANGAR Brno"],
    "Hlavní nádraží": ["Koliště", "Špilberk", "Winning Group Arena", "Stránska skála"],
    "HANGAR Brno": ["Winning Group Arena"],
    "Stránska skála": ["Hlavní nádraží"]
}

def test_path(start: str, goal: str, profile: str):
    router = CyclingRouter(LOCATIONS, ROAD_NETWORK, PROFILES)
    if not router.is_symmetric_network():
        return

    distance, path, elevation = router.a_star(start, goal, profile)

    if path == []:
        print("A path from", start, "to", goal, "does not exist")
        return

    print("Chosen profile:", profile)
    print("Optimal path:", ' -> '.join(path))
    print("Elevation gained:", round(elevation, 2), "m")
    print("Overall distance:", round(distance / 1000, 2), "km")
    print ()


if __name__ == "__main__":
    test_path("Prygl", "HANGAR Brno", "flat")
    test_path("Prygl", "HANGAR Brno", "mountain")
o", "mountain")
