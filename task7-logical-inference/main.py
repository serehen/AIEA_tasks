# bird(X) :- feathers(X).
# bird(X) :- flies(X), lays_eggs(X).
# penguin(X) :- bird(X), no_flight(X), swims(X), black_white(X).

def backchain_tree(clause):
    #opus is a penguin

    # works recursively on lists of any nested depth
    if isinstance(clause, list):
        # list check, if yes then call recursively on separate items
        new_list = []
        for item in clause:
            new = backchain_tree(item)
            new_list.append(new)
        # new_list.insert(0, clause)
        return [new_list]

    # checks kb to see if 
    requirements = kb(clause)

    if requirements is not None:
        reqlist = []
        for i, item in enumerate(requirements):
            new = backchain_tree(item)
            if isinstance(new, list):
                for j, new_item in enumerate(new):
                    reqlist.insert(i+j, new_item)
            else:
                reqlist.append(new)
        chain = [clause]
        chain.append(reqlist)
        return chain
    else:
        # no further requirements in kb 
        return clause            

def entails(goal, entity, seen=None):
    # avoids cycles by returning upon seeing duplicate statement
    if seen is None:
        seen = set()
    key = (goal, entity)
    if key in seen:
        return False
    seen.add(key)

    # grabs facts pertaining to entity
    facts = kb(entity)
    if facts is not None and goal in facts:
        return True

    # grabs rules for goal
    rule_reqs = kb(goal)
    if rule_reqs is None:
        return False

    # checks for nesting and recursively checks requirements for goal
    has_nested = any(isinstance(item, list) for item in rule_reqs)
    if has_nested:
        for item in rule_reqs:
            if isinstance(item, list):
                if all(entails(sub, entity, seen.copy()) for sub in item):
                    return True
            else:
                if entails(item, entity, seen.copy()):
                    return True
        return False
    else:
        return all(entails(item, entity, seen.copy()) for item in rule_reqs)

# def backchain_parser(tree):
#     parsed = []
#     for i, item in enumerate(tree):
#         if isinstance(item, list):
#             if i > 0:
#                 parsed.append('or')
#             parse = backchain_parser(item)
#             parsed.append(parse)
#         elif i > 0:
#             parsed.append('and')
#             parsed.append(item)
#         else:
#             parsed.append(item)
#     return parsed
        

def kb(x):
    if x == 'tim':
        return ['feathers', 'flies']
    elif x == 'bird':
        return ['feathers', ['flies', 'lays eggs']]
    elif x == 'penguin':
        return ['bird', 'no flight', 'swims', 'black and white']
    else:
        return None

# print(backchain_tree('penguin'))
# print(backchain_parser(backchain_tree('penguin')))
print(entails('penguin', 'tim'))