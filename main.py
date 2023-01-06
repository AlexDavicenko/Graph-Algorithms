import pygame
import sys
import pickle

from threading import Thread
from string import ascii_uppercase

from visualisation_colors import Colors
from graph import Node, Edge, UndirectedWeightedEdge, DirectedWeightedEdge, bfs
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
    fps = 144
    speed = 2

    def __init__(self):
        Thread(target=self.cli_thread).start()

        self.node_radius = 30
        self.nodes = []
        self.edges = []

        self.highlighted_nodes = []
        self.highlighted_edges = []

        self.window = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.selected_node = None

        self.NODE_LABEL_FONT = pygame.font.SysFont("arial", 20)

        self.visualising = False
        self.ticks_left = 0
        self.visualisation_generator = None

    def save(self):
        with open("saves/graph.pickle", "wb") as f:
            f.write(pickle.dumps(
                (self.nodes, self.edges)
            ))

    def load(self):
        with open("saves/graph.pickle", "rb") as f:
            self.nodes, self.edges = f.read(pickle.loads(f.read()))

    def cli_thread(self):
        while True:
            cmd = input("$ ")
            if not cmd:
                continue

            tokens = [token.strip() for token in cmd.strip().split(" ")] + [""]*8
            print(tokens)
            if tokens[0] == "quit":
                self.close()
            elif tokens[0] == "help":
                return
            elif tokens[0] == "run":
                if tokens[1] == "bfs":
                    start_node = self.get_node_from_name(tokens[2])
                    end_node = self.get_node_from_name(tokens[3])
                    if start_node:
                        if end_node:
                            self.run_bfs(start_node, end_node)
                    elif self.selected_node:
                        self.run_bfs(self.selected_node)

    def get_node_from_name(self, name):
        for node in self.nodes:
            if node.name == name.upper():
                return node

    def run_bfs(self, start, target=None):

        self.visualising = True
        self.ticks_left = 200
        self.visualisation_generator = bfs(start, target)
        self.selected_node = None


    def close(self):
        pygame.quit()
        sys.exit()

    def generate_node_label(self):
        text = ""
        if len(self.nodes) < 26:
            text = ascii_uppercase[len(self.nodes)]
        elif len(self.nodes) < 26**2:
            text = ascii_uppercase[(len(self.nodes) % 26)] + ascii_uppercase[len(self.nodes) // 26]
        return text, self.NODE_LABEL_FONT.render(text, True, (0, 0, 0))

    def run_visualisations(self):
        if self.visualising:
            print(self.ticks_left)
            if self.ticks_left <= 0:
                self.ticks_left = 200/self.speed
                try:
                    next(self.visualisation_generator)
                except StopIteration:
                    self.visualising = False

            else:
                self.ticks_left += -1

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
                    for node in self.nodes:
                        if (node.x - mx) ** 2 + (node.y - my) ** 2 < self.node_radius ** 2:
                            clicked_node = node
                        if (node.x-mx)**2+(node.y-my)**2 < 4*self.node_radius**2:
                            overlapping = True

                    if self.selected_node:
                        if not clicked_node:
                            self.selected_node = None
                        else:
                            if clicked_node != self.selected_node:
                                dist = Node.get_euclidean_distance(self.selected_node, clicked_node)
                                label = self.NODE_LABEL_FONT.render(str(int(dist)), True, self.EDGE_LABEL_COLOR)
                                self.edges.append(UndirectedWeightedEdge(self.selected_node, clicked_node, self.EDGE_COLOR, dist, label))

                                self.selected_node = None

                    else:
                        if clicked_node:
                            self.selected_node = clicked_node
                        elif not overlapping:
                            name, label = self.generate_node_label()
                            self.nodes.append(
                                Node(mx, my, label, name, self.NODE_COLOR)
                            )

            if event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "b":
                    if self.selected_node:
                        self.run_bfs(self.selected_node)

                if pygame.key.name(event.key) == "n":
                    if self.selected_node:
                        print(self.selected_node.get_neighbours())


    def render(self):
        # Order
        # Background -> Edges -> Edge labels -> Edge line -> Nodes -> Node Labels -> Selected Node
        self.window.fill((255, 255, 255))

        # Edges
        for edge in self.edges:
            pygame.draw.line(
                self.window,
                edge.color,
                (edge.node1.x, edge.node1.y),
                (edge.node2.x, edge.node2.y),
                3
            )
            # Edge Labels
            self.window.blit(edge.label, edge.label_rect)
        # Edge line
        if self.selected_node:
            mx, my = pygame.mouse.get_pos()
            pygame.draw.line(self.window, (120,120,120), (self.selected_node.x, self.selected_node.y), (mx, my), 3)
        # Nodes
        for node in self.nodes:
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
        if self.selected_node:
            pygame.draw.circle(
                self.window,
                self.NODE_SELECTED_BORDER_COLOR,
                (self.selected_node.x, self.selected_node.y),
                self.node_radius
            )
            pygame.draw.circle(
                self.window,
                self.selected_node.color,
                (self.selected_node.x, self.selected_node.y),
                self.node_radius-2
            )
            # Rerender the selected node label
            node_label_rect = self.selected_node.label.get_rect()
            node_label_rect.center = (self.selected_node.x, self.selected_node.y)

            self.window.blit(self.selected_node.label, node_label_rect)

        pygame.display.update()


    def handle_fps(self):
        self.clock.tick(self.fps)

    def main_loop(self):
        while True:
            self.handle_fps()

            self.eventloop()
            self.run_visualisations()

            self.render()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Graph Visualisation")
    Visualisation().main_loop()
