men_pref = {
    "A":["X", "Z", "Y"],
    "B":["Z", "X", "Y"],
    "C":["Y", "Z", "X"]
}
women_pref = {
    "X":["A", "B", "C"],
    "Y":["B", "A", "C"],
    "Z":["C", "A", "B"]
}
women = [w for w in women_pref.keys()]
men = [m for m in men_pref.keys()]