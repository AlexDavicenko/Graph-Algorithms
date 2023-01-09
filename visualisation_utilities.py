

class VisualisationUtility:
    def __init__(self, graph_object):

        self.graph = graph_object
        self.visualising = False
        self.visualisation_generator = None

        self.ticks_left = 0
        self.speed = 1


    def run_visualisations(self):
        if self.visualising:
            if self.ticks_left <= 0:
                self.ticks_left = 200/self.speed
                try:
                    next(self.visualisation_generator)
                except StopIteration:
                    self.visualising = False

            else:
                self.ticks_left += -1

    def run_algorithm(self, generator, *args, **kwargs):
        self.visualising = True
        self.visualisation_generator = generator(self.graph, *args, **kwargs)
        self.graph.selected_node = None

