import CSP

csp = CSP.CSP()

#csp.add_vertex('heino', [0,1,2,3,4])
#csp.add_vertex('marko', [0,1,2,3,4])
#csp.add_vertex('lurk', [0,1,2,3,4])
csp.add_vertex('heino', [0,1,2])
csp.add_vertex('marko', [0,1,2])
csp.add_vertex('lurk', [0,1,2])
csp.add_vertex('anderes1', [8, 5])
csp.add_vertex('anderes2', [5,6,7])
csp.add_vertex('anderes3', [5,6,7])


csp.add_bi_edge(('marko', 'heino', lambda x, y: x == y))
csp.add_bi_edge(('heino', 'lurk', lambda x, y: x == y))
csp.add_bi_edge(('lurk', 'marko', lambda x, y: x == y))
csp.add_bi_edge(('lurk', 'lurk', lambda v: v == 1))

csp.permutate_and_shuffle("anderes1 anderes2 anderes3".split(), lambda x, y: x > 5)
#csp.add_bi_edge(('lurk', 'marko', lambda x, y: x != y))

#csp.check_soundness()

solution = csp.solve()

print('\n'+ 'Solution = ' + '\n' + str(solution))
