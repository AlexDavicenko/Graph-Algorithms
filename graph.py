from visualisation_colors import Colors


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.selected_node = None

    def clear_screen(self):
        self.nodes = []
        self.edges = []

    def reset(self):
        for node in self.nodes:
            node.reset()
        for edge in self.edges:
            edge.reset()

    def get_node_from_name(self, name):
        for node in self.nodes:
            if node.name == name.upper():
                return node


class Node(Colors):

    def __getstate__(self):
        return {
            "x": self.x,
            "y": self.y,
            "name": self.name,
            "color": self.color,
            "edges": self.edges,
            "label": None
        }
    def __setstate__(self, state):
        self.__dict__ = state

    @staticmethod
    def get_euclidean_distance(node1, node2):
        return ((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2) ** 0.5

    @staticmethod
    def get_manhattan_distance(node1, node2):
        return abs(node1.x-node2.x) + abs(node1.y-node2.y)


    def __init__(self, x, y, name, color):
        self.x = x
        self.y = y
        self.name = name
        self.color = color

        self.edges = []
        self.label = None
    def set_label(self, label):
        self.label = label

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_neighbours(self):
        neighbours = []
        for edge in self.edges:
            if isinstance(edge, DirectedEdge):
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
            if isinstance(edge, DirectedEdge):
                if edge.node2 == neighbour:
                    return edge
            else:
                if edge.node1 == neighbour or edge.node2 == neighbour:
                    return edge

    def set_as_start(self):
        self.color = self.START_COLOR

    def set_as_end(self):
        self.color = self.END_COLOR

    def reset(self):
        self.color = self.NODE_COLOR

    def visit(self):
        if self.color == self.START_COLOR or self.color == self.END_COLOR:
            return
        self.color = self.NODE_VISITED_COLOR

    def visited(self):
        return self.color == self.NODE_VISITED_COLOR


# Undirected Unweighted Edge
class Edge(Colors):
    def __init__(self, node1, node2, color, name = ""):
        self.node1 = node1
        self.node2 = node2
        self.color = color
        self.name = name

        self.label = None
        self.label_rect = None
        self.add_edges()

    def add_edges(self):
        self.node1.add_edge(self)
        self.node2.add_edge(self)

    def visit(self):
        self.color = self.EDGE_VISITED_COLOR

    def set_label(self, label):
        self.label = label
    def reset(self):
        self.color = self.EDGE_COLOR

    def is_visited(self):
        return self.color == self.EDGE_VISITED_COLOR

    def set_rect_center(self):
        self.label_rect = self.label.get_rect()
        self.label_rect.center = ((self.node1.x + self.node2.x) // 2, (self.node1.y + self.node2.y) // 2)

    def __getstate__(self):
        return {
            "node1": self.node1,
            "node2": self.node2,
            "color": self.color,
            "name": self.name,
            "label": None,
            "label_rect": None
        }

    def __setstate__(self, state):
        self.__dict__ = state

# Undirected Weighted edge
class WeightedEdge(Edge):

    def __init__(self, node1, node2, color, weight):

        super().__init__(node1, node2, color, name = str(int(weight)))

        self.weight = weight

    def __getstate__(self):
        return {
            "node1": self.node1,
            "node2": self.node2,
            "color": self.color,
            "name": self.name,
            "weight": self.weight,
            "label": None,
            "label_rect": None
        }

    def __setstate__(self, state):
        self.__dict__ = state

# Directed edge
class DirectedEdge(Edge):
    def __init__(self, node1, node2, color, weight, label):
        super().__init__(node1, node2, color, weight)

    def add_edges(self):
        self.node1.add_edge(self.node2)

# Directed Weighted edge
class DirectedWeightedEdge(Edge):
    def __init__(self):
        super().__init__()

def bfs(start_node: Node, target: Node):
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

def dfs(start_node, target):
    start_node.set_as_start()
    stack = [start_node]
    visited = set()

    while stack:
        node = stack.pop()

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

                stack.append(neighbour)
