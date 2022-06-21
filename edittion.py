import random
import networkx as nx

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

        """
        Done in a way that distance graph[current_position][next_position]:

                    next
                    1   2   3   4   5   6   7

        curr 1      dist  dist  dist  dist dist 
             2      etc .....  .... etc.... 
             3      if None = doesnt exist
             4
             5
             6
             7
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
        self.pheromone_evaporation_coefficient = 0.06
        self.ants = [self.Ant() for _ in range(ant_amount)]
        self.pheromone_delta = 1.5

    class Ant:
        def __init__(self):
            self.visited_nodes: list[int] = []
            self.distance_traveled: float = 0
            self.current_node: int = 0
            self.alpha: float = 10.0
            self.beta: float = 10.0
            self.first_run = True
            self.in_finish_node = False
            self.possible_connections = []

        def choose_path(self, graph) -> int:

            target_nodes: list[float] = graph.distance_graph[self.current_node]


            possible_connections = [target_nodes[i]
                                         for i in range(len(target_nodes))
                                         if target_nodes[i] > 0 and i not in self.visited_nodes]

            pheromones_connected: list[float] = graph.pheromone_graph[self.current_node]

            # for each path calculate probability percent

            if self.first_run:

                import random
                return target_nodes.index(random.choice(possible_connections))



            attractiveness = dict()
            sum_total = 0.0

            for i in range(0, len(possible_connections)):
                pheromone_amount = float(pheromones_connected[i])
                distance = float(possible_connections[i])
                # log("distance: " + str(distance) + " , amount: " + str(pheromone_amount))
                attractiveness[i] = (pow(pheromone_amount, self.alpha) * pow(1 / distance, self.beta))
                sum_total += attractiveness[i]


            if sum_total != 0.0:
                weightsList = [attractiveness[i]/sum_total for i in range(len(possible_connections))]
            else:
                weightsList = None

            import random
            return target_nodes.index(random.choices(possible_connections, weights = weightsList, k=1)[0])

        def get_distance_traveled(self):
            return self.distance_traveled


        def traverse(self, start, end, graph: Graph):
            """
            _update_route() to show new traversal
            _update_distance_traveled() to record new distance traveled
            self.location update to new location
            called from run()
            """
            self.update_route(end)
            self.update_distance_traveled(start, end, graph)
            self.current_node = end

        def update_route(self, new):
            """
            add new node to self.route
            remove new node form self.possible_location
            called from _traverse() & __init__()
            """
            self.visited_nodes.append(new)
            try:
                self.possible_connections.remove(new)
            except ValueError:
                print("tried to remove ", new)

        def update_distance_traveled(self, start, end, graph: Graph):
            """
            use self.distance_callback to update self.distance_traveled
            """
            log("distance added: " + str(graph.distance_graph[start][end]))
            self.distance_traveled += graph.distance_graph[start][end]
            log("distance current: " + str(self.distance_traveled))



    def update_pheromone(self, graph: Graph):

        n = len(graph.pheromone_graph[0])

        new_pheromone_graph = [[0 for _ in range(n)] for _ in range(n)]

        for ant in self.ants:
            for i in range(len(ant.visited_nodes) - 1):
                begin = ant.visited_nodes[i]
                end = ant.visited_nodes[i + 1]
                current_pheromone = graph.pheromone_graph[begin][end]
                new_pheromone_value = self.pheromone_delta / ant.get_distance_traveled()
                new_pheromone_graph[begin][end] = current_pheromone + new_pheromone_value
                new_pheromone_graph[begin][end] = current_pheromone + new_pheromone_value
                log("new_pheromone: " + str(new_pheromone_graph[begin][end]))
        for start in range(n):
            for end in range(n):

                graph.pheromone_graph[start][end] = (1 - self.pheromone_evaporation_coefficient) * \
                                                 graph.pheromone_graph[start][end]

                # then add all contributions to this location for each ant that travered it
                # (ACO)
                # tau_xy <- tau_xy + delta tau_xy_k
                #	delta tau_xy_k = Q / L_k
                graph.pheromone_graph[start][end] += new_pheromone_graph[start][end]




    def reset_ants(self, graph):
        for ant in self.ants:
            ant.__init__()
            ant.possible_connections = [i for i in range(1, len(graph.distance_graph[0]))
                                        if i != ant.current_node]

    def place_ants(self, place):
        for ant in self.ants:
            ant.current_node = place
            ant.visited_nodes.append(place)


    def run(self, graph, starting_node, finish_node, iterations):








        import matplotlib.pyplot as plt
        import networkx as nx
        import numpy as np


        G = nx.from_numpy_matrix(np.matrix(graph.pheromone_graph))
        for i in range(len(graph.pheromone_graph[0])):
            for j in range(len(graph.pheromone_graph[0])):
                if graph.distance_graph[i][j] > 0:
                    G.add_edge(i, j, weight= round(graph.distance_graph[i][j],3))


        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

        pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
        nx.draw_networkx_edges(
            G, pos, edgelist=esmall, width=6, alpha=1, edge_color="b", style="dashed"
        )

        # node labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()












        graph = graph
        self.place_ants(starting_node)

        for ant in self.ants:
            ant.possible_connections = [i
                                        for i in range(len(graph.distance_graph[0]))
                                        if i != ant.current_node]

        self.finish_node = finish_node

        for _ in range(iterations):
            self.move_all(graph)
            self.update_pheromone(graph)
            self.reset_ants(graph)
            self.place_ants(starting_node)

    def move_all(self, graph):
        for ant in self.ants:

            while ant.possible_connections and not ant.in_finish_node:
                next_node = ant.choose_path(graph)
                log("next: "+str(next_node))
                ant.traverse(ant.current_node, next_node, graph)


                if ant.current_node == self.finish_node:
                    ant.in_finish_node = True


            ant.first_run = False
            log(ant.visited_nodes)



            # log("finished")
            # log("ant chosen " + str(ant.current_node) + " and previous was " + str(ant.previous_node))
            # self._update_route(end)
            # self._update_distance_traveled(start, end)
            # self.location = end














testGraph = Graph(10)
testGraph.print_graph()







testColony = AntColony(100)
testColony.run(testGraph, 0, 4, 1000)
