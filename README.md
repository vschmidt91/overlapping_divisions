# Matchmaking with overlapping divisions

## Goals

On the Starcraft 2 AI Discord, there has been discussion about matchmaking systems for the AIArena ladder and what makes them good or bad. Most of these have been adressed by the addition of divisions thanks to Infy, Immodal and others. These goals include:

1. more meaningful games for high ranked authors
2. providing meaningful challenge for lower ranked authors
3. a sense of achievement as bots progress up the ladder
4. all bots should get roughly the same number of matches

## Assessment

While 1, 2 and 4 seem generally agreed on as being achieved by the current matchmaker, side effects that seem unintended or even counter to these goals have been verbalized:

*Note: I feel confident talking about this because my highest ranking bot benefited strongly from both of these effects.*

- **Bot performance can be highly dependent on division count.**
ELO movements upwards of 100 have been observed after changing from 2 to 3 divisions as they suddenly face different opponents. That way, a bots movement (progression) can be largely or entirely superseded by having parameters of the competition change, which is arguably the opposite of goal 3. https://discord.com/channels/350289306763657218/350290846320427011/961198070224269312

- **Progression speed is severely decreased at the top or bottom of a division.**
As a bot moves towards the top of its division, it faces (almost) exclusively bots with lower rating that yield little to no gain but heavy downside. Similarly, downward movement at the bottom of a division is very slow.
https://discord.com/channels/350289306763657218/350290846320427011/961200726338576384
The effect of this is subjective. Making something artificially harder than it already is could result in a greater sense of achievement. However promotions and demotions are often only temporary anyway ("ELO mules"). The lasting effect is that ladder progression is noticably faster in the middle of a division than at the boundaries.

## Proposal

- keep division system as it is
- queue matches between adjacent divisions
- optionally: increase division count

## Comparison

The code compares the two systems by considering

1. **Relevancy**: The difference between the rank of a bot and its average opponent (avg_rank_diff)
(this corresponds to goals 1 and 2, and is also at the core of the described side effects)
2. **Fairness**: The difference of the min/max number of matches per bot (max_match_diff)
(corresponding to goal 4)
3.  **Variety**: The number of unique opponents a bot faces (avg_opponent_count)

The code in this repository shows that overlapping divisions are better both in terms of relevancy and variety of games, while faring a little worse in terms of fairness.

## Results

no overlap, num_divisions= 3

|   num_bots |   max_match_diff |   avg_rank_diff |   avg_opponent_count |
|------------|------------------|-----------------|----------------------|
|         50 |                1 |         5.89796 |              15.68   |
|         51 |                0 |         6       |              16      |
|         52 |                1 |         6.12    |              16.3462 |
|         53 |                1 |         6.23077 |              16.6792 |
|         54 |                0 |         6.33333 |              17      |
|         55 |                1 |         6.45283 |              17.3455 |
|         56 |                1 |         6.56364 |              17.6786 |
|         57 |                0 |         6.66667 |              18      |
|         58 |                1 |         6.78571 |              18.3448 |
|         59 |                1 |         6.89655 |              18.678  |
|         60 |                0 |         7       |              19      |
|         61 |                1 |         7.11864 |              19.3443 |
|         62 |                1 |         7.22951 |              19.6774 |
|         63 |                0 |         7.33333 |              20      |
|         64 |                1 |         7.45161 |              20.3438 |
|         65 |                1 |         7.5625  |              20.6769 |
|         66 |                0 |         7.66667 |              21      |
|         67 |                1 |         7.78462 |              21.3433 |
|         68 |                1 |         7.89552 |              21.6765 |
|         69 |                0 |         8       |              22      |

overlap, num_divisions= 6

|   num_bots |   max_match_diff |   avg_rank_diff |   avg_opponent_count |
|------------|------------------|-----------------|----------------------|
|         50 |                2 |         5.35052 |              20.8    |
|         51 |                3 |         5.48949 |              21.3725 |
|         52 |                3 |         5.61758 |              21.9231 |
|         53 |                2 |         5.736   |              22.4528 |
|         54 |                1 |         5.85809 |              23      |
|         55 |                3 |         5.91111 |              23.2364 |
|         56 |                2 |         5.96024 |              23.4643 |
|         57 |                3 |         6.09823 |              24.0351 |
|         58 |                3 |         6.22654 |              24.5862 |
|         59 |                2 |         6.34615 |              25.1186 |
|         60 |                1 |         6.46903 |              25.6667 |
|         61 |                3 |         6.52137 |              25.9016 |
|         62 |                2 |         6.57025 |              26.129  |
|         63 |                3 |         6.70743 |              26.6984 |
|         64 |                3 |         6.83591 |              27.25   |
|         65 |                2 |         6.95649 |              27.7846 |
|         66 |                1 |         7.08    |              28.3333 |
|         67 |                3 |         7.13178 |              28.5672 |
|         68 |                2 |         7.18045 |              28.7941 |
|         69 |                3 |         7.31698 |              29.3623 |
