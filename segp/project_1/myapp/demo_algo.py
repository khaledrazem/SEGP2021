def all_subset(query):
    from itertools import combinations
    subset = []
    if len(query) > 2:
        for i in set(combinations(query, r=2)):
            subset.append(i)
        for i in set(combinations(query, r=1)):
            subset.append(i)
    else:
        for i in set(combinations(query, r=1)):
            subset.append(i)
    return subset