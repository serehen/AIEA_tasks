import janus_swi as janus

janus.consult("KB.pl")

tests = [
    # Facts
    ("male(homer)", True),
    ("male(bart)", True),
    ("male(lisa)", False),

    ("female(marge)", True),
    ("female(lisa)", True),
    ("female(bart)", False),

    ("parent(homer,bart)", True),
    ("parent(mona,homer)", True),
    ("parent(bart,homer)", False),

    # Derived
    ("mother(marge,bart)", True),
    ("father(homer,lisa)", True),
    ("mother(homer,bart)", False),
    ("father(marge,lisa)", False),

    ("son(bart,homer)", True),
    ("daughter(lisa,marge)", True),
    ("son(lisa,homer)", False),
    ("daughter(bart,marge)", False),

    ("grandparent(abe,bart)", True),
    ("grandparent(mona,lisa)", True),
    ("grandparent(marge,bart)", False),
]

passed = 0
failed = 0

for query, expected in tests:
    try:
        res = janus.query_once(query)
        got = bool(res.get("truth")) if isinstance(res, dict) else bool(res)

        if got == expected:
            print(f"PASS {query} -> {got}")
            passed += 1
        else:
            print(f"FAIL {query} -> got {got}, expected {expected} | raw={res}")
            failed += 1
    except Exception as e:
        print(f"ERROR | {query} -> {e}")
        failed += 1

print(f"\nSummary: passed={passed}, failed={failed}, total={len(tests)}")