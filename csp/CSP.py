import copy


class CSP:
    def __init__(self):
        self.edge_count = 0
        self.vertex_count = 0
        self.edges = []
        self.vertex_2_index = dict()
        self.index_2_vertex = dict()
        self.vertices = dict()
        self.domain = dict()

    def add_edge(self, edge):
        self.edges.append(edge)
        self.edge_count += 1

    def add_bi_edge(self, edge):
        self.add_edge(edge)
        self.add_edge((edge[1],edge[0],edge[2]))

    def add_vertex(self, name, domain):
        self.vertices[name] = domain
        self.domain[name] = domain
        self.vertex_2_index[name] = self.vertex_count
        self.index_2_vertex[self.vertex_count] = name
        self.vertex_count += 1

    def nc(self):   # optimierbar
        for v in self.vertices.keys():
            to_delete = set({})
            deleted = False
            for x in self.vertices[v]:
                for e in self.edges:
                    if e[0] == v and e[1] == v:
                        if not e[2](x):
                            if x in self.vertices[v]:
                                deleted = True
                                to_delete.add(x)
            if deleted:
                for x in to_delete:
                    self.vertices[v].remove(x)

    def revise(self, e):
        delete = False
        to_delete = []
        source = e[0]
        target = e[1]
        constraint = e[2]
        for x in self.vertices[source]:
            is_consistent = False
            for y in self.vertices[target]:
                if constraint(x, y):
                    is_consistent = True
            if not is_consistent:
                to_delete.append(x)
                delete = True
        for elem in to_delete:
            self.vertices[e[0]].remove(elem)
        return delete

    def ac3_la(self, cv):
        cv_filter = lambda v1, v2, current: \
            (self.vertex_2_index[v1] > current) and (self.vertex_2_index[v2] == current)
        q = {e for e in self.edges if cv_filter(e[0], e[1], cv)}                # Q <- {(Vi,Vcv) in arcs(G),i>cv};
        consistent = True
        while not len(q) == 0 and consistent:                                   # while not Q empty & consistent
            test_e = q.pop()                                                    # select and delete arc (Vk,Vm) from Q
            if self.revise(test_e):
                q.update({e for e in self.edges if
                          (self.index_of(e[0]) != self.index_of(e[1]))          # Q <- Q union {(Vi,Vk) such that
                          and (self.index_of(e[0]) != self.index_of(test_e[1])) # (Vi,Vk) in arcs(G),i#k,i#m,i>cv}
                          and (self.index_of(e[0]) > cv)})
                consistent = not len(self.vertices[test_e[0]]) == 0             # consistent <- not Dk empty
        return consistent

    def ac3(self):
        ne_filter = lambda v1, v2: (self.vertex_2_index[v1] != self.vertex_2_index[v2])
        q = {e for e in self.edges if ne_filter(e[0], e[1])}
        while not len(q) == 0:
            test_e = q.pop()
            if self.revise(test_e):
                q.update({e for e in self.edges if
                          (self.index_of(e[0]) != self.index_of(e[1])) and
                          (self.index_of(e[0]) != self.index_of(test_e[1]))})

    def solve_rek(self, cv):
        current_vertex = self.index_2_vertex[cv]
        current_domain = self.vertices[current_vertex]
        if len(current_domain) == 0:                            # Abbruchkriterium, trigger backtracking
            return False
        state = copy.deepcopy(self.vertices)                    # capture state
        self.vertices[current_vertex] = [current_domain.pop()]  # pflücke value aus aktueller domain
        if self.ac3_la(cv):                                     # teste ac3, falls success   -> next cv (knoten)
            if cv == self.vertex_count - 1:
                return True                                     # Loesung gefunden
            if self.solve_rek(cv + 1):                          # Knoten-Wert-Paar ok: pruefe naechsten Knoten
                return True                                                # falls fail -> wiederherstellen und next value
        self.vertices = state                                   # restore state
        self.vertices[current_vertex] = current_domain
        return self.solve_rek(cv)

    def solve(self):
        self.nc()                                               # unaere constraints anwenden
        self.ac3()                                              # kantenkonsistenz herstellen
        if self.solve_rek(0):                                   # loesungsalgorithmus aufrufen
            return self.vertices
        return False

    def index_of(self, v):
        return self.vertex_2_index[v]

    def permutate_and_shuffle(self, vertices, constraint):
        for x in vertices:
            for y in vertices:
                if x != y:
                    self.add_edge((x, y, constraint))