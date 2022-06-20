import random

DEBUG = True


def log(s):
    if DEBUG:
        print(s)


class Graph:
    def __init__(self, n):

        self.n: int = n

        self.distance_graph: list[list[float]] = [[random.SystemRandom().uniform(0, 10) for _ in range(n)] for _ in
                                                  range(n)]

        for _ in range(n // 2):
            x: int = random.randint(0, n - 1)
            y: int = random.randint(0, n - 1)
            self.distance_graph[x][y] = -1

        for i in range(self.n):
            self.distance_graph[i][i] = 0
            for j in range(self.n):
                self.distance_graph[i][j] = self.distance_graph[j][i]

        self.pheromone_graph: list[list[float]] = [[0 for _ in range(n)] for _ in range(n)]

    def add_edge(self, u, v, w):
        self.distance_graph[u][v] = w
        self.distance_graph[v][u] = w

    def print_graph(self):
        for i in range(len(self.distance_graph)):
            print(self.distance_graph[i])

    def get_size_of_graph(self):
        return self.n


class AntColony:
    def __init__(self, ant_amount):
        self.finish_node = -1
        self.ants = [self.Ant() for _ in range(ant_amount)]
        self.pheromone_delta = 1.5

    class Ant:
        def __init__(self):
            self.traversed_path: list[int] = []
            self.distance_traveled: float = 0
            self.current_node: int = -1
            self.previous_node: int = -1
            self.alpha: float = 10.0
            self.beta: float = 10.0
            self.first_run = True
            self.in_finish_node = False
            self.possible_connections = []

        def choose_path(self, graph) -> int:
            distances_connected = graph.distance_graph[self.current_node]
            self.possible_connections = [distances_connected[i]
                                         for i in range(len(distances_connected))
                                         if distances_connected[i] > 0 and i not in self.traversed_path]
            pheromones_connected: list[float] = graph.pheromone_graph[self.current_node]
            if self.first_run or sum(pheromones_connected) == 0:
                chosen = self.current_node
                counter = 0
                while (distances_connected[chosen] <= 0) or (chosen in self.traversed_path) or chosen == 0:
                    chosen = random.randint(0, len(distances_connected) - 1)
                    counter += 1
                    if counter > 100:
                        self.in_finish_node = False
                        return self.previous_node
                return chosen
            else:
                attractiveness = dict()
                sum_total = 0.0
                for i in range(0, len(distances_connected)):
                    if distances_connected[i] > 0:
                        pheromone_amount = float(pheromones_connected[i])
                        distance = float(distances_connected[i])
                        attractiveness[i] = (pow(pheromone_amount, self.alpha) * pow(1 / distance, self.beta))
                        sum_total += attractiveness[i]
                toss = random.uniform(0, sum_total)
                cummulative = 0
                for possible_next_location in attractiveness:
                    weight = (attractiveness[possible_next_location] / sum_total)
                    if (toss <= weight + cummulative) and (possible_next_location not in self.traversed_path) and \
                            distances_connected[possible_next_location] > 0:
                        return possible_next_location
                    cummulative += weight
                self.in_finish_node = False
                return self.previous_node

        def reset(self, place, graph):
            self.traversed_path = []
            self.distance_traveled = 0
            self.current_node = place
            self.previous_node = place
            self.in_finish_node = False
            self.first_run = True
            distances_connected = graph.distance_graph[self.current_node - 1]
            self.possible_connections = [distances_connected[i]
                                         for i in range(len(distances_connected))
                                         if i > 0 and i not in self.traversed_path]

        def delete_path(self, graph):
            node1 = self.traversed_path[-2]
            if len(self.traversed_path) >= 3:
                node2 = self.traversed_path[-3]
            else:
                node2 = 0
            graph.distance_graph[node1][node2] = -1

        def get_distance_traveled(self):
            return self.distance_traveled

    def update_pheromone(self, graph: Graph):

        for ant in self.ants:
            if self.finish_node:
                for i in range(len(ant.traversed_path) - 1):
                    begin = ant.traversed_path[i]
                    end = ant.traversed_path[i + 1]
                    current_pheromone = graph.pheromone_graph[begin][end]
                    new_pheromone_value = self.pheromone_delta / ant.get_distance_traveled()
                    graph.pheromone_graph[begin][end] = current_pheromone + new_pheromone_value
                    graph.pheromone_graph[end][begin] = current_pheromone + new_pheromone_value

    def reset_ants(self, place):
        for ant in self.ants:
            ant.traversed_path = []
            ant.distance_traveled = 0
            ant.current_node = place
            ant.previous_node = place
            ant.alpha = 10.0
            ant.beta = 10.0
            ant.in_finish_node = False
            ant.possible_connections = []

    def place_ants(self, place):
        for ant in self.ants:
            ant.current_node = place
            ant.previous_node = place

    def run(self, graph, starting_node, finish_node, iterations):
        graph.distance_graph[starting_node][finish_node] = -1
        graph.distance_graph[finish_node][starting_node] = -1

        self.place_ants(starting_node)

        self.finish_node = finish_node

        for _ in range(iterations):
            self.move_all(graph, starting_node)
            self.update_pheromone(graph)

        most = 0
        most_num = 0
        for ant in self.ants:
            most_temp = 0
            for ant2 in self.ants:
                if ant.traversed_path == ant2.traversed_path:
                    most_temp += 1
            if most_temp > most_num:
                most_num = most_temp
                most = ant

        log(str(most.traversed_path))
        log(most_num)

    def move_all(self, graph, place):
        self.reset_ants(place)
        for ant in self.ants:
            distances_connected = graph.distance_graph[ant.current_node - 1]
            ant.possible_connections = [distances_connected[i]
                                        for i in range(len(distances_connected))
                                        if i > 0 and i not in ant.traversed_path]
            while ant.possible_connections and not ant.in_finish_node:
                ant.previous_node = ant.current_node
                ant.current_node = ant.choose_path(graph)
                ant.traversed_path.append(ant.current_node)
                if ant.previous_node is not None and ant.current_node is not None:
                    ant.distance_traveled += graph.distance_graph[ant.previous_node][ant.current_node]

                if ant.current_node == self.finish_node:
                    ant.in_finish_node = True

                if ant.previous_node == ant.current_node:
                    ant.delete_path(graph)
                    ant.reset(place, graph)

            if ant.first_run:
                ant.first_run = False


testGraph = Graph(7)
testColony = AntColony(10000)
testColony.run(testGraph, 0, 4, 300)
