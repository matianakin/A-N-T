import random

DEBUG = True


def log(s):
    if DEBUG:
        print(s)


class Graph:
    def __init__(self, n):
        self.n: int = n
        self.distance_graph: list[list[float]] = [[random.SystemRandom().uniform(0, 10) for i in range(n)] for j in
                                                  range(n)]
        self.pheromone_graph: list[list[float]] = [[0 for i in range(n)] for j in range(n)]

        """
        Done in a way that distance graph[current_position][next_position]:
        
                    next
                    A   B   C   D   E   F   G
        
        curr A      dist  dist  dist  dist dist 
             B      etc .....  .... etc.... 
             C
             D
             E
             F
             G
        """

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
        self.graph = None
        self.ants = [self.Ant() for n in range(ant_amount)]
        self.pheromone_delta = 0
        self.first_run = True

    class Ant:
        def __init__(self):
            self.current_node: int = -1
            self.previous_node: int = -1
            self.alpha: float = 10.0
            self.beta: float = 10.0

    def choose_path(self, ant: Ant) -> int:

        distances_connected: list[float] = self.graph.distance_graph[ant.current_node]
        pheromones_connected: list[float] = self.graph.pheromone_graph[ant.current_node]
        # for each path calculate probability percent

        if self.first_run:
            import random
            chosen = ant.current_node
            while chosen == ant.current_node:
                chosen = random.randint(0, len(distances_connected))
            return chosen

        attractiveness = dict()
        sum_total = 0.0

        for i in range(0, len(distances_connected)):
            pheromone_amount = float(pheromones_connected[i])
            distance = float(distances_connected[i])

            # tau^alpha * eta^beta
            attractiveness[i] = pow(pheromone_amount, ant.alpha) * pow(1 / distance, ant.beta)
            sum_total += attractiveness[i]

            # cumulative probability behavior, inspired by: http://stackoverflow.com/a/3679747/5343977
            # randomly choose the next path
            import random
            toss = random.random()

            cummulative = 0
            for possible_next_location in attractiveness:
                weight = (attractiveness[possible_next_location] / sum_total)
                if toss <= weight + cummulative:
                    return possible_next_location
                cummulative += weight

        import random
        toss = random.random()










    def place_ants(self, place):
        for ant in self.ants:
            ant.current_node = ant.previous_node = place

    def run(self, graph):
        # while 1:
        self.graph = graph
        self.move_all()

        self.first_run = False

    def move_all(self):
        for ant in self.ants:
            ant.previous_node = ant.current_node
            ant.current_node = self.choose_path(ant)
            log("ant chosen " + str(ant.current_node) + " and previous was " + str(ant.previous_node))




testGraph = Graph(15)
testGraph.print_graph()
testColony = AntColony(100)
testColony.place_ants(0)
testColony.run(testGraph)
