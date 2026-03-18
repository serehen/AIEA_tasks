import janus_swi as janus
janus.consult('KB.pl')

print('parent check')
#parent(X, Y). to check in swiprolog
for p_rel in janus.query('parent(X, Y)'):
    print(p_rel)
print('son check')
#son(X, Y). to check in swiprolog
for s_rel in janus.query('son(X, Y)'):
    print(s_rel.get('Y'))
print('daughter check')
#daughter(X,Y). to check in swiprolog
for d_rel in janus.query('daughter(X, Y)'):
    print(d_rel.get('Y'))
