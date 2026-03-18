# bird(X) :- feathers(X).
# bird(X) :- flies(X), lays_eggs(X).
# penguin(X) :- bird(X), no_flight(X), swims(X), black_white(X).

def backchain_tree(clause):
    #opus is a penguin

    # works recursively on lists of any nested depth (i think)
    if type(clause) == list:
        # list check, if yes then call recursively on separate items
        new_list = []
        for item in clause:
            new = backchain_tree(item)
            new_list.append(new)
        # new_list.insert(0, clause)
        return new_list

    # checks kb to see if 
    requirements = kb(clause)

    if requirements is not None:
        reqlist = []
        for item in requirements:
            new = backchain_tree(item)
            reqlist.append(new)
        chain = [clause]
        chain.append(reqlist)
        return chain
    else:
        # no further requirements in kb 
        return clause            

def backchain_solve(clause, X):
    # determining whether clause applies to entity X

    data = kb(X)

    if data == None:
        return False
    
    requirements = backchain_tree(clause)
    for item in data:
        if item in requirements:
            



def kb(x):
    if x == 'tim':
        return ['feathers', 'flies']
    elif x == 'bird':
        return [['feathers'], ['flies', 'lays eggs']]
    elif x == 'penguin':
        return ['bird', 'no flight', 'swims', 'black and white']
    else:
        return None

print(backchain_tree('penguin'))