import pygame
import pygame.gfxdraw
import sys
import pickle

from arrows import draw_arrow

from threading import Thread

from visualisation_colors import Colors
from visualisation_utilities import VisualisationUtility
from graph import Graph, Node, Edge, WeightedEdge, DirectedEdge, DirectedWeightedEdge
from graph import bfs, dfs, dijkstra
"""
#Checks complete, connected , bipartite, Eulearian, Hamiltonian,
#Prims algorithm
#TSP algorithms
#refactor functionality into different files


#and parsing commands (regex)

#Directed and undirected mode (console options)

#Arrows
#Implement color start end 
# modes


# fix arrows
# bezier curves for double weighted edges
"""


class Visualisation(Colors):
    @staticmethod
    def close():
        pygame.quit()
        sys.exit()

    def __init__(self):
        Thread(target=self.cli_thread).start()

        self.window = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()


        self.NODE_LABEL_FONT = pygame.font.SysFont("arial", 20)

        self.node_radius = 30
        self.graph = Graph()
        self.visualisation_utility = VisualisationUtility(self.graph)

        self.numerical_labels = False
        self.mode = "edit"
        self.edges_type = {
            "weighted": True,
            "directed": True
        }

        self.load("graph.pickle")

    def reconstruct_labels(self):
        for node in self.graph.nodes:
            node.set_label(self.NODE_LABEL_FONT.render(node.name, True, self.NODE_LABEL_COLOR))
        for edge in self.graph.edges:
            edge.set_label(self.NODE_LABEL_FONT.render(edge.name, True, self.EDGE_LABEL_COLOR))
            edge.set_rect_center()

    def save(self, name):

        # Removing unpickable pygame object
        for node in self.graph.nodes:
            node.label = None
        for edge in self.graph.edges:
            edge.label = None
            edge.label_rect = None

        with open(f"saves/{name}", "wb") as f:
            f.write(pickle.dumps(self.graph))

        self.reconstruct_labels()

    def load(self, name):
        with open(f"saves/{name}", "rb") as f:
            self.graph = pickle.loads(f.read())
            self.visualisation_utility = VisualisationUtility(self.graph)

            self.graph.reset()
            self.reconstruct_labels()
            print(f"Loaded {name}")
    def cli_thread(self):
        while True:
            cmd = input("$ ")
            if not cmd:
                continue

            tokens = [token.strip() for token in cmd.strip().split(" ")] + [""]*8
            print(tokens)

            match tokens[0]:
                case "quit":
                    self.close()
                case "help":
                    return
                case "load":
                    if tokens[1]:
                        self.load(tokens[1])
                case "save":
                    if tokens[1]:
                        self.save(tokens[1])
                case "clear":
                    self.graph.clear_screen()
                case "mode":
                    match tokens[1]:
                        case "edit":
                            self.mode = "edit"
                        case "run":
                            self.mode = "run"
                case "reset":
                    self.graph.reset()
                case "labels":
                    match tokens[1]:
                        case "numerical":
                            self.numerical_labels = True
                        case "alphanumerical":
                            self.numerical_labels = False
                case "run":
                    match tokens[1]:
                        case "bfs":
                            start_node = self.graph.get_node_from_name(tokens[2])
                            end_node = self.graph.get_node_from_name(tokens[3])
                            if start_node:
                                if end_node:
                                    self.visualisation_utility.run_algorithm(bfs)
                            elif self.graph.selected_node:
                                self.visualisation_utility.run_algorithm(bfs)

                        case "dijkstra":
                            start_node = self.graph.get_node_from_name(tokens[2])
                            end_node = self.graph.get_node_from_name(tokens[3])

                            if start_node and end_node:
                                self.graph.start_node = start_node
                                self.graph.end_node = end_node
                                self.visualisation_utility.run_algorithm(dijkstra)

    def generate_node_label(self, font):
        nodes_placed = len(self.graph.nodes)

        if self.numerical_labels:
            return str(nodes_placed+1), font.render(str(nodes_placed+1), True, (0, 0, 0))

        else:
            a_offset = ord("A")
            text = ""
            if nodes_placed < 26:
                text = chr(a_offset + nodes_placed)
            elif nodes_placed < 26**2:
                text = chr(a_offset + (nodes_placed % 26)) + chr(a_offset + nodes_placed // 26)
            return text, font.render(text, True, (0, 0, 0))
    def create_weighted_edge(self, node1, node2):

        dist = Node.get_euclidean_distance(node1, node2)
        label = self.NODE_LABEL_FONT.render(str(int(dist)), True, self.EDGE_LABEL_COLOR)
        edge = WeightedEdge(node1, node2, dist)
        edge.set_label(label)
        edge.set_rect_center()
        self.graph.edges.append(edge)
        edge.set_label(label)

    def create_edge(self, node1,node2):
        self.graph.edges.append(
            Edge(node1, node2)
        )
    def create_directed_edge(self, node1, node2):
        self.graph.edges.append(
            DirectedEdge(node1, node2)
        )
    def create_directed_weighted_edge(self, node1, node2):
        dist = Node.get_euclidean_distance(node1, node2)
        label = self.NODE_LABEL_FONT.render(str(int(dist)), True, self.EDGE_LABEL_COLOR)
        edge = DirectedWeightedEdge(node1, node2, dist)
        edge.set_label(label)
        edge.set_rect_center()
        self.graph.edges.append(edge)
        edge.set_label(label)

    def create_node(self, x, y):
        name, label = self.generate_node_label(self.NODE_LABEL_FONT)
        node = Node(x, y, name)
        self.graph.nodes.append(
            node
        )
        node.set_label(label)

    def eventloop(self):
        mx, my = pygame.mouse.get_pos()

        m_keys = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            # Close window
            if event.type == pygame.QUIT:
                self.close()


            if event.type == pygame.MOUSEBUTTONUP:
                if m_keys[0]:

                    # Checking for overlap or node click
                    clicked_node = None
                    overlapping = False
                    for node in self.graph.nodes:
                        distance_squared = (node.x - mx) ** 2 + (node.y - my) ** 2
                        if distance_squared < self.node_radius ** 2:
                            clicked_node = node
                        if distance_squared < 4*self.node_radius**2:
                            overlapping = True

                    if self.mode == "edit":
                        # If already selected node
                        if self.graph.selected_node:
                            # Deselect (clicked on empty space)
                            if not clicked_node:
                                self.graph.selected_node = None
                            # Clicked a different node
                            else:
                                # Create Edge
                                if clicked_node != self.graph.selected_node:
                                    if self.edges_type["weighted"] and self.edges_type["directed"]:
                                        self.create_directed_weighted_edge(self.graph.selected_node, clicked_node)
                                    elif self.edges_type["weighted"]:
                                        self.create_weighted_edge(self.graph.selected_node, clicked_node)
                                    elif self.edges_type["directed"]:
                                        self.create_directed_edge(self.graph.selected_node, clicked_node)
                                    else:
                                        self.create_edge(self.graph.selected_node, clicked_node)


                                    self.graph.selected_node = None
                        else:
                            # Select clicked node
                            if clicked_node:
                                self.graph.selected_node = clicked_node

                            # Create node
                            if not clicked_node and not overlapping:
                                self.create_node(mx, my)

            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "b":
                    if self.graph.selected_node:
                        self.visualisation_utility.run_algorithm(bfs)

                if pygame.key.name(event.key) == "n":
                    if self.graph.selected_node:
                        print(self.graph.selected_node.get_neighbours())


    def render(self):
        # Order
        # Background -> Edges -> Edge labels -> Edge line -> Nodes -> Node Labels -> Selected Node
        self.window.fill((255, 255, 255))

        # Edges
        for edge in self.graph.edges:
            pygame.draw.line(
                self.window,
                edge.color,
                (edge.node1.x, edge.node1.y),
                (edge.node2.x, edge.node2.y),
                5
            )
            #Arrows
            if isinstance(edge, DirectedEdge):
                u = 0.75
                x1 = edge.node1.x
                y1 = edge.node1.y
                x2 = edge.node2.x
                y2 = edge.node2.y
                ux, uy = x1 + u * (x2 - x1), y1 + u * (y2 - y1)

                draw_arrow(self.window, pygame.Vector2(x1,y1), pygame.Vector2(ux, uy), (0,0,0), head_height= 25, head_width=25)
                #pygame.draw.polygon(self.window, edge.color, edge.arrow_points)

            # Edge Labels
            self.window.blit(edge.label, edge.label_rect)
        # Edge line
        if self.graph.selected_node and self.mode == "edit":
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(self.window, (120,120,120), (self.graph.selected_node.x, self.graph.selected_node.y), (mx, my), 5)
        # Nodes
        for node in self.graph.nodes:
            pygame.gfxdraw.aacircle(self.window,node.x,node.y, self.node_radius, self.NODE_BORDER_COLOR)
            """
            pygame.draw.circle(
                self.window,
                self.NODE_BORDER_COLOR,
                (node.x, node.y),
                self.node_radius,
            )
            pygame.draw.circle(
                self.window,
                node.color,
                (node.x, node.y),
                self.node_radius-2,
            )
            """
            # Node labels
            if node.label:
                node_label_rect = node.label.get_rect()
                node_label_rect.center = (node.x, node.y)
                self.window.blit(node.label, node_label_rect)

        # Selected node highlight
        if self.graph.selected_node:
            pygame.draw.circle(
                self.window,
                self.NODE_SELECTED_BORDER_COLOR,
                (self.graph.selected_node.x, self.graph.selected_node.y),
                self.node_radius
            )
            pygame.draw.circle(
                self.window,
                self.graph.selected_node.color,
                (self.graph.selected_node.x, self.graph.selected_node.y),
                self.node_radius-2
            )
            # Render the selected node label again
            node_label_rect = self.graph.selected_node.label.get_rect()
            node_label_rect.center = (self.graph.selected_node.x, self.graph.selected_node.y)

            self.window.blit(self.graph.selected_node.label, node_label_rect)

        pygame.display.update()

    def main_loop(self):
        while True:

            self.eventloop()
            self.visualisation_utility.run_visualisations()

            self.render()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Graph Visualisation")
    Visualisation().main_loop()
