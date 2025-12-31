men_pref = {
    "M1": ["W1", "W2", "W3"],
    "M2": ["W2", "W3", "W1"],
    "M3": ["W3", "W1", "W2"]
}

women_pref = {
    "W1": ["M2", "M1", "M3"],
    "W2": ["M1", "M2", "M3"],
    "W3": ["M3", "M1", "M2"]
}
men = [m for m in men_pref.keys()]
women = [w for w in women_pref.keys()]

# All possible permutations of women (3! = 6)
permutations = [
    ["W1", "W2", "W3"],
    ["W1", "W3", "W2"],
    ["W2", "W1", "W3"],
    ["W2", "W3", "W1"],
    ["W3", "W1", "W2"],
    ["W3", "W2", "W1"]
]

for perm in permutations:
    pairs = [[men[i], perm[i]] for i in range(len(men))]
    stable = True
    for m, w in pairs:
        for wi in women:
            if wi == w:
                continue
            m2 = [x for x, y in pairs if y == wi][0]
            if men_pref[m].index(wi) < men_pref[m].index(w) and women_pref[wi].index(m) < women_pref[wi].index(m2):
                stable = False
                break
        if not stable:
            break
    if stable:
        print("Stable matching:", pairs)