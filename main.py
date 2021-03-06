
from collections import Counter
from tabulate import tabulate

def create_divisions(num_bots, num_divisions):
    
    # goal is uniform division size
    size = num_bots // num_divisions

    # but generally, some divisions will need to be 1 bigger
    remainder = num_bots - num_divisions * size
    division_sizes = remainder * [size+1] + (num_divisions - remainder) * [size]

    # the only proposed change to the division system:
    # at parity, put the bigger divisions at top and bottom
    # (still works without, but matches are distributed less equal)
    division_sizes.append(division_sizes.pop(0))

    divisions = []
    s = 0
    for i in range(num_divisions):
        n = division_sizes[i]
        divisions.append(list(range(s, s + n)))
        s += n
    return divisions

def create_matches_with_overlap(divs):

    matches = []

    for i in range(len(divs) - 1):
        matches.extend(create_matches_for_division(divs[i] + divs[i+1]))

    # first and last division have no divisions above/below to overlap with
    # => match them against themselves
    matches.extend(create_matches_for_division(divs[0]))
    matches.extend(create_matches_for_division(divs[0]))
    matches.extend(create_matches_for_division(divs[-1]))
    matches.extend(create_matches_for_division(divs[-1]))

    return matches


def create_cyclic_matches(num_bots):
    k = 10
    l = list(range(1, num_bots - 1, 2))
    r = list(range(2, num_bots - 1, 2))
    cycle = [0] + l + [num_bots-1] + r[::-1]
    for i, a in enumerate(cycle):
        for j in range(i - k, i + k + 1):
            if i == j:
                continue
            yield a, cycle[j % len(cycle)]

def create_matches_without_overlap(divs):
    matches = []
    for d in divs:
        matches.extend(create_matches_for_division(d))
    return matches

def create_matches_for_division(div):
    for i, a in enumerate(div):
        for b in div[i+1:]:
            yield a, b

"""count the number of matches per bot and get the difference between min/max. Lower values = greater fairness in terms of server share"""
def get_max_match_diff(matches):
    counter = Counter((bot for match in matches for bot in match))
    counts = set(counter.values())
    return max(counts) - min(counts)

"""get the average number of unique opponenents per bot. Higher values = greater variety of opponents"""
def get_avg_opponent_count(num_bots, matches):
    opponents = [[(a if b == i else b) for (a, b) in matches if i in (a, b)] for i in range(num_bots)]
    opponent_counts = [len(set(opps)) for opps in opponents]
    return sum(opponent_counts) / len(opponent_counts)

"""get the average rank difference among the matches. Lower values = more relevant matches"""
def get_avg_rank_diff(matches):
    return sum(abs(a - b) for a, b in matches) / len(matches)

num_divisions = 3

headers = ['num_bots', 'max_match_diff', 'avg_rank_diff', 'avg_opponent_count', 'num_matches']
table_without_overlap = []
table_with_overlap = []
table_cyclic = []
table_format = 'github'

for num_bots in range(50, 70):

    row = [num_bots]
    divisions = create_divisions(num_bots, 2 * num_divisions)
    matches = create_matches_with_overlap(divisions)
    row.append(get_max_match_diff(matches))
    row.append(get_avg_rank_diff(matches))
    row.append(get_avg_opponent_count(num_bots, matches))
    row.append(len(matches))
    table_with_overlap.append(row)

    row = [num_bots]
    divisions = create_divisions(num_bots, num_divisions)
    matches = create_matches_without_overlap(divisions)
    row.append(get_max_match_diff(matches))
    row.append(get_avg_rank_diff(matches))
    row.append(get_avg_opponent_count(num_bots, matches))
    row.append(len(matches))
    table_without_overlap.append(row)

    row = [num_bots]
    matches = list(create_cyclic_matches(num_bots))
    row.append(get_max_match_diff(matches))
    row.append(get_avg_rank_diff(matches))
    row.append(get_avg_opponent_count(num_bots, matches))
    row.append(len(matches))
    table_cyclic.append(row)


print('overlap, num_divisions=', 2*num_divisions)
print(tabulate(table_with_overlap, headers=headers, tablefmt=table_format))


print('no overlap, num_divisions=', num_divisions)
print(tabulate(table_without_overlap, headers=headers, tablefmt=table_format))

print('cyclic')
print(tabulate(table_cyclic, headers=headers, tablefmt=table_format))