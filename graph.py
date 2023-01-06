from visualisation_colors import Colors


class Node(Colors):
    @staticmethod
    def get_euclidean_distance(node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

    @staticmethod
    def get_manhattan_distance(node1, node2):
        return abs(node1.x-node2.x) + abs(node1.y-node2.y)


    def __init__(self, x, y, label, name, color):
        self.x = x
        self.y = y
        self.label = label
        self.name = name
        self.color = color
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_neighbours(self):
        neighbours = []
        for edge in self.edges:
            if isinstance(edge, DirectedWeightedEdge):
                if self == edge.node1:
                    neighbours.append(edge.node2)
            else:
                if self == edge.node1:
                    neighbours.append(edge.node2)
                if self == edge.node2:
                    neighbours.append(edge.node1)
        return neighbours

    def get_edge(self, neighbour):
        for edge in self.edges:
            if isinstance(edge, DirectedWeightedEdge):
                if edge.node2 == neighbour:
                    return edge
            else:
                if edge.node1 == neighbour or edge.node2 == neighbour:
                    return edge

    def set_as_start(self):
        self.color = self.START_COLOR

    def set_as_end(self):
        self.color = self.END_COLOR

    def visit(self):
        if self.color == self.START_COLOR or self.color == self.END_COLOR:
            return
        self.color = self.NODE_VISITED_COLOR

    def visited(self):
        return self.color == self.NODE_VISITED_COLOR
# Undirected Unweighted Edge


class Edge(Colors):
    def __init__(self, node1, node2, color):
        self.node1 = node1
        self.node2 = node2
        self.color = color

        self.add_edges()

    def add_edges(self):
        self.node1.add_edge(self)
        self.node2.add_edge(self)

    def visit(self):
        self.color = self.EDGE_VISITED_COLOR

    def is_visited(self):
        return self.color == self.EDGE_VISITED_COLOR

class UndirectedWeightedEdge(Edge):
    def __init__(self, node1, node2, color, weight, label):

        super().__init__(node1, node2, color)
        self.weight = weight

        self.label = label
        self.label_rect = label.get_rect()
        self.label_rect.center = ((node1.x + node2.x)//2, (node1.y+node2.y)//2)


class DirectedWeightedEdge(UndirectedWeightedEdge):
    def __init__(self, node1, node2, color, weight, label):
        super().__init__(node1, node2, color, weight, label)

    def add_edges(self):
        self.node1.add_edge(self.node2)


def bfs(start_node, target):
    start_node.set_as_start()
    queue = [start_node]
    visited = set()

    while queue:
        node = queue.pop(0)

        if node == target:
            node.set_as_end()
            break

        # Visualising node visit
        node.visit()
        yield

        visited.add(node)

        for neighbour in node.get_neighbours():

            # Visualising
            edge = node.get_edge(neighbour)
            if not edge.is_visited():
                edge.visit()
                yield

            if neighbour not in visited:

                queue.append(neighbour)
