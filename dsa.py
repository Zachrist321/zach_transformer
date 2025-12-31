
men = {
    "A": ["Y", "Z", "X"],
    "B": ["Z", "Y", "X"],
    "C": ["Y", "X", "Z"]
}

women = {
    "X": ["B", "A", "C"],
    "Y": ["C", "A", "B"],
    "Z": ["A", "B", "C"]
}

# Track engagements
engaged_to = {}
free_men = [m for m in men.keys()]
next_proposal = {"A": 0, "B": 0, "C": 0}

# Precompute ranking for women
ranking = {w: {m: i for i, m in enumerate(prefs)} for w, prefs in women.items()}

while free_men:
    m = free_men.pop(0)
    w = men[m][next_proposal[m]]
    next_proposal[m] += 1
    print(f"{m} proposes to {w}")

    if w not in engaged_to:
        engaged_to[w] = m
        print(f"{w} was free and accepts {m}")
    else:
        current = engaged_to[w]
        if ranking[w][m] < ranking[w][current]:
            print(f"{w} prefers {m} over {current}. {current} is now free.")
            engaged_to[w] = m
            free_men.append(current)
        else:
            print(f"{w} rejects {m} (prefers {current})")
            free_men.append(m)

print("\nFinal matching:")
for w, m in engaged_to.items():
    print(f"{m} — {w}")
