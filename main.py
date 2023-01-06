import pygame
import sys
import pickle

from threading import Thread
from string import ascii_uppercase

from visualisation_colors import Colors
from visualisation_utilities import VisualisationUtility
from graph import Graph, Node, Edge, WeightedEdge
"""
#Add nodes
#Add weights
#Checks complete, connected , bipartite, Eulearian, Hamiltonian,
#Prims algorithm
#TSP algorithms

#Input through terminal via 2 threads
#and parsing commands (regex)

#Directed and undirected mode (console options)

#Saving graphs
#Implement a command stack
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


    def save(self, name):

        with open(f"saves/{name}", "wb") as f:
            f.write(pickle.dumps(self.graph))

    def load(self, name):
        with open(f"saves/{name}", "rb") as f:
            self.graph = pickle.loads(f.read())
            self.visualisation_utility = VisualisationUtility(self.graph)

            self.graph.reset()
            for node in self.graph.nodes:
                node.set_label(self.NODE_LABEL_FONT.render(node.name, True, self.NODE_LABEL_COLOR))
            for edge in self.graph.edges:
                edge.set_label(self.NODE_LABEL_FONT.render(edge.name, True, self.EDGE_LABEL_COLOR))
                edge.set_rect_center()
            print("asdasdasdasd")
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

                case "run":
                    match tokens[1]:
                        case "bfs":
                            start_node = self.graph.get_node_from_name(tokens[2])
                            end_node = self.graph.get_node_from_name(tokens[3])
                            if start_node:
                                if end_node:
                                    self.visualisation_utility.run_bfs(start_node, end_node)
                            elif self.graph.selected_node:
                                self.visualisation_utility.run_bfs(self.graph.selected_node)



    def generate_node_label(self, font):
            nodes_placed = len(self.graph.nodes)
            a_offset = ord("A")
            text = ""
            if nodes_placed < 26:
                text = chr(a_offset + nodes_placed)
            elif nodes_placed < 26**2:
                text = chr(a_offset + (nodes_placed % 26)) + chr(a_offset + nodes_placed // 26)
            return text, font.render(text, True, (0, 0, 0))


    def eventloop(self):
        mx, my = pygame.mouse.get_pos()

        m_keys = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            if event.type == pygame.MOUSEBUTTONUP:
                if m_keys[0]:

                    clicked_node = None
                    overlapping = False
                    for node in self.graph.nodes:
                        distance_squared = (node.x - mx) ** 2 + (node.y - my) ** 2
                        if distance_squared < self.node_radius ** 2:
                            clicked_node = node
                        if distance_squared < 4*self.node_radius**2:
                            overlapping = True

                    if self.graph.selected_node:
                        if not clicked_node:
                            self.graph.selected_node = None
                        else:
                            # Create edge
                            if clicked_node != self.graph.selected_node:
                                dist = Node.get_euclidean_distance(self.graph.selected_node, clicked_node)
                                label = self.NODE_LABEL_FONT.render(str(int(dist)), True, self.EDGE_LABEL_COLOR)
                                edge = WeightedEdge(self.graph.selected_node, clicked_node, self.EDGE_COLOR, dist)
                                edge.set_label(label)
                                edge.set_rect_center()
                                self.graph.edges.append(edge)
                                edge.set_label(label)

                                self.graph.selected_node = None

                    else:
                        if clicked_node:
                            self.graph.selected_node = clicked_node
                        elif not overlapping:
                            # Create node
                            name, label = self.generate_node_label(self.NODE_LABEL_FONT)
                            node = Node(mx, my, name, self.NODE_COLOR)
                            self.graph.nodes.append(
                                node
                            )
                            node.set_label(label)

            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "b":
                    if self.graph.selected_node:
                        self.visualisation_utility.run_bfs(self.graph.selected_node)

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
            # Edge Labels
            self.window.blit(edge.label, edge.label_rect)
        # Edge line
        if self.graph.selected_node:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(self.window, (120,120,120), (self.graph.selected_node.x, self.graph.selected_node.y), (mx, my), 5)
        # Nodes
        for node in self.graph.nodes:
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
            # Node labels
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
