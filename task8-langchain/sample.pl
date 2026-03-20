mammal(lion).
mammal(wolf).
mammal(elephant).
bird(eagle).
bird(hawk).
fish(shark).
fish(salmon).
reptile(cobra).

savanna(lion).
savanna(elephant).
forest(wolf).
ocean(shark).
ocean(salmon).

carnivore(lion).
carnivore(wolf).
herbivore(elephant).

neighbors(X, Y) :- 
    (savanna(X), savanna(Y); forest(X), forest(Y); ocean(X), ocean(Y)), 
    X \= Y.

warm_blooded(A) :- 
    mammal(A); 
    bird(A).

cold_blooded(A) :- 
    fish(A); 
    reptile(A).

at_risk(Prey, Hunter) :- 
    herbivore(Prey), 
    carnivore(Hunter), 
    neighbors(Prey, Hunter).

is_aquatic(A) :- 
    fish(A); 
    ocean(A).

land_dweller(A) :- 
    (mammal(A); reptile(A)), 
    not(ocean(A)).