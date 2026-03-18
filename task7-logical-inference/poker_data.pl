# transitivity
beats(two-pair, pair).
beats(three-of-a-kind, two-pair).
beats(straight, three-of-a-kind).
beats(flush, straight).
beats(full_house, flush).
beats(straight-flush, full_house).

beat_better(X, Y) :- beats(X, Y).
beat_better(X, Y) :- beats(X, Z), beat_better(Z, Y).

#relational rule set
person(x).
person(y).
person(z).

parent(x, y).

sibling(X, Y) :- parent(Z, X), parent(Z, Y),  X \= Y.
child(X, Y) :- parent(Y, X).
cousin(X, Y) :- parent(Z, X), parent(A, Y), sibling(A, Z).
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
granchild(X, Y) :- parent(Z, X), parent(Y, Z).

# backward chaining
bird(opus)
swims(opus)

bird(X) :- feathers(X).
bird(X) :- flies(X), lays_eggs(X).
penguin(X) :- bird(X), no_flight(X), swims(X), black_white(X).
