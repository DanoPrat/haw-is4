import math
import pprint
import CSP

def dom():
    return [0,1,2,3,4]

csp = CSP.CSP()

# variablen
csp.add_vertex('brite', dom())
csp.add_vertex('schwede', dom())
csp.add_vertex('daene', dom())
csp.add_vertex('norweger', dom())
csp.add_vertex('deutscher', dom())

csp.add_vertex('rot', dom())
csp.add_vertex('gruen', dom())
csp.add_vertex('gelb', dom())
csp.add_vertex('weiss', dom())
csp.add_vertex('blau', dom())

csp.add_vertex('hund', dom())
csp.add_vertex('vogel', dom())
csp.add_vertex('katze', dom())
csp.add_vertex('pferd', dom())
csp.add_vertex('fisch', dom())

csp.add_vertex('tee', dom())
csp.add_vertex('kaffee', dom())
csp.add_vertex('milch', dom())
csp.add_vertex('bier', dom())
csp.add_vertex('wasser', dom())

csp.add_vertex('pallmall', dom())
csp.add_vertex('dunhill', dom())
csp.add_vertex('marlboro', dom())
csp.add_vertex('winfield', dom())
csp.add_vertex('rothmanns', dom())

# constraints
gleich = lambda x, y: x == y
ungleich = lambda x, y: x != y
mittelhaus = lambda x: x == 2
nachbarn = lambda x, y: math.fabs(x-y) == 1
linksvon = lambda x, y: x < y
rechtsvon = lambda x, y: x > y
ersteshaus = lambda x: x == 0

## unaer
csp.add_bi_edge(('milch', 'milch', mittelhaus))     #7
csp.add_bi_edge(('norweger', 'norweger', ersteshaus)) #9

## binaer
csp.add_bi_edge(('brite', 'rot', gleich))           #1
csp.add_bi_edge(('schwede', 'hund', gleich))        #2
csp.add_bi_edge(('daene', 'tee', gleich))           #3
csp.add_edge(('gruen', 'weiss', linksvon))          #4.1
csp.add_edge(('weiss', 'gruen', rechtsvon))         #4.2
csp.add_bi_edge(('gruen', 'kaffee', gleich))        #5
csp.add_bi_edge(('pallmall', 'vogel', gleich))      #6
csp.add_bi_edge(('gelb', 'dunhill', gleich))        #8
csp.add_bi_edge(('winfield', 'bier', gleich))       #12
csp.add_bi_edge(('deutscher', 'rothmanns', gleich)) #14
csp.add_bi_edge(('marlboro', 'katze', nachbarn))    #10
csp.add_bi_edge(('pferd', 'dunhill', nachbarn))     #11
csp.add_bi_edge(('norweger', 'blau', nachbarn))     #13
csp.add_bi_edge(('marlboro', 'wasser', nachbarn))   #15

## global
nationen = "brite schwede daene norweger deutscher".split()
farben = "rot gruen gelb weiss blau".split()
tiere = "hund vogel katze pferd fisch".split()
getraenke = "tee kaffee milch bier wasser".split()
zigaretten = "pallmall dunhill marlboro winfield rothmanns".split()

csp.permutate_and_shuffle(nationen, ungleich)
csp.permutate_and_shuffle(farben, ungleich)
csp.permutate_and_shuffle(tiere, ungleich)
csp.permutate_and_shuffle(getraenke, ungleich)
csp.permutate_and_shuffle(zigaretten, ungleich)

#csp.check_soundness()

solution = csp.solve()

# Ausgabe
if solution != False:
    inv_solution = {0: [], 1: [], 2: [], 3: [], 4: []}

    for k, v in solution.items():
        inv_solution[v[0]].append(k)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(inv_solution)
else:
    print("\nKeine Loesung gefunden")

