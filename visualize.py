import numpy as np
import networkx as nx
import math


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, alpha):
        return Vector(self.x * alpha, self.y * alpha)

    __rmul__ = __mul__

    def __truediv__(self, alpha):
        self.x /= alpha
        self.y /= alpha
        return self

    def get(self):
        return self.x, self.y

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm_square(self):
        return self.x ** 2 + self.y ** 2


class Node():
    def __init__(self, id, neighbors, x, y):
        self.id = id
        self.neighbors = neighbors
        self.point = Vector(x, y)


def ForceDirectedAlgorithm():
    G = nx.read_gexf('vk-friends-358564550_.gexf')
    N = G.number_of_nodes()
    nodes = []
    mapping = dict(zip(G, range(N)))
    G = nx.relabel_nodes(G, mapping)

    np.random.RandomState(42)
    for i in range(N):
        x = np.random.random() * 100
        y = np.random.random() * 100
        neighbors = [n for n in G.neighbors(i)]
        nodes.append(Node(i, neighbors, x, y))

    C = 0.2
    K = 1

    def Add(i, j):
        return (nodes[i].point + nodes[j].point)

    def Sub(i, j):
        return (nodes[i].point - nodes[j].point)

    def NormSquare(i, j):
        return (nodes[i].point - nodes[j].point).norm_square()

    def Norm(i, j):
        return (nodes[i].point - nodes[j].point).norm()

    def Fr(i, j):
        return - C * (K ** 2) / Norm(i, j)

    def Fa(i, j):
        return NormSquare(i, j) / K


    converged = False
    tol = 1e-6
    step = 10
    t = 0.9
    energy = float('Inf')
    progress = 0

    def UpdateStepLength(step, energy, energy_, progress):
        if energy < energy_:
            progress += 1
            if progress >= 5:
                progress = 0
                step = step / t
        else:
            progress = 0
            step = step * t
        return step, progress


    while not converged:
        ds = 0.
        energy_ = energy
        energy = 0
        for i in range(N):
            f = Vector(0., 0.)
            for j in nodes[i].neighbors:
                f = f + (Fa(i, j) / Norm(i, j)) * Sub(j, i)
            for j in range(i):
                f = f + (Fr(i, j) / Norm(i, j)) * Sub(j, i)
            for j in range(i + 1, N):
                f = f + (Fr(i, j) / Norm(i, j)) * Sub(j, i)
            nodes[i].point += step / f.norm() * f
            ds += (step / f.norm() * f).norm_square()
            energy += f.norm_square()
        step, progress = UpdateStepLength(step, energy, energy_, progress)
        if math.sqrt(ds) < K * tol:
            converged = True

    pos = {}
    for i in range(N):
        pos[i] = nodes[i].point.get()
    nx.draw(G, pos=pos)


ForceDirectedAlgorithm()