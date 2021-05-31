'''
Realizing graph colorizing by backtracking.
'''


def read_file(path):
    '''
    Reads from file and converts info into graph.
    '''
    with open(path) as file:
        lines = file.readlines()

    lines = [x for x in lines]
    new_lines = []
    for line in lines:
        new_line = line.strip().split(" ")
        new_lines.append(new_line)

    return new_lines


class Graph:
    '''
    Represents a graph.
    '''
    class Vertex:
        '''
        Represents a vertex of the graph.
        '''

        def __init__(self, number, color=None):
            '''
            Initializes class.
            '''
            self.number = number
            self.color = color

        def __hash__(self):
            return hash(self.number)

        def __str__(self):
            '''
            Returns information about vertex in string.
            '''
            return f"Vertex(number:{self.number}, color:{self.color})"

    def __init__(self, new_lines, num_colors):
        '''
        Initializes class.
        '''
        self.new_lines = new_lines
        self.num_colors = num_colors
        graph = dict()
        vertexes = {}
        for i in range(len(new_lines)):
            vertexes[i] = self.Vertex(i)

        for listik in new_lines:
            for element in listik:
                if element == '1':
                    if not vertexes[self.new_lines.index(listik)
                                    ] in graph:
                        graph[vertexes[self.new_lines.index(listik)
                                       ]] = []
                    graph[vertexes[self.new_lines.index(listik)
                                   ]].append(vertexes[listik.index(element)])
                    listik[listik.index(element)] = '0'

            else:
                continue

        self.graph = graph

    def is_safe(self, num_vertex, col):
        '''
        Checks if it is ok to set the given colour to the given vertex.
        '''

        for key in self.graph.keys():
            if key.number == num_vertex:
                for val in self.graph[key]:
                    if val.color == col:
                        return False
        return True

    def graph_color_recursive(self, num_colors, num_vertex):
        '''
        Recursive function to colorize the graph by backtracking.
        '''
        if num_vertex == len(self.graph.keys()):
            return True

        for col in range(1, num_colors + 1):
            if self.is_safe(num_vertex, col) == True:
                for key in self.graph.keys():
                    if key.number == num_vertex:
                        key.color = col
                if self.graph_color_recursive(num_colors, num_vertex + 1) == True:
                    return True

    def graph_color_final(self):
        '''
        Shows result of the colorizing.
        '''
        if self.graph_color_recursive(self.num_colors, 0) == None:
            return "It is not possible to colour given graph in this number of colours."

        print("Solution exists and here are the assigned colours:")
        for vertex in self.graph.keys():
            print(vertex)
        return "Congratulations!"


if __name__ == "__main__":
    graph = Graph(read_file("data/graph_matrix.txt"), 4)
    print(graph.graph_color_final())
