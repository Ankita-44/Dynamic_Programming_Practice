# Domino + L-tromino tiling of 2 x n board
# dp by column with a 2-bit mask for the current column.
# Returns number of tilings of 2 x n (mod mod if provided).

from functools import lru_cache

H = 2  # height

def gen_transitions():
    """Precompute transitions: for each current_mask (0..3) return list of possible next_mask values."""
    all_trans = [[] for _ in range(1 << H)]
    patterns = [
        # L-trominos as list of (row, col_offset) where col_offset 0=current, 1=next
        # Four L shapes (3 cells each) in a 2x2 block
        [(0,0),(1,0),(0,1)],  # missing (1,1)
        [(0,0),(1,0),(1,1)],  # missing (0,1)
        [(0,0),(0,1),(1,1)],  # missing (1,0)
        [(1,0),(0,1),(1,1)],  # missing (0,0)
    ]
    full_mask = (1 << H) - 1  # 0b11

    for start_mask in range(1 << H):
        results = set()
        # DFS: mask_cur shows filled bits in current column so far (start with start_mask).
        # next_mask accumulates occupancies in next column.
        def dfs(mask_cur, next_mask):
            if mask_cur == full_mask:
                results.add(next_mask)
                return
            # find first empty row in current column
            for r in range(H):
                if not (mask_cur >> r) & 1:
                    row = r
                    break

            # 1) Place horizontal domino: occupies (row, current) and (row, next)
            if not ( (next_mask >> row) & 1 ):
                dfs(mask_cur | (1 << row), next_mask | (1 << row))

            # 2) Place vertical domino (only possible if other row also free)
            other = 1 - row
            if not ( (mask_cur >> other) & 1 ):
                # place vertical domino filling both rows of current column
                dfs(mask_cur | (1 << row) | (1 << other), next_mask)

            # 3) Place L-trominos that include (row, current). Check each pattern that contains this cell.
            for patt in patterns:
                # only consider patterns that include (row,0) to avoid duplicates
                if (row,0) not in patt:
                    continue
                ok = True
                new_mask_cur = mask_cur
                new_next_mask = next_mask
                for (rr, co) in patt:
                    if co == 0:
                        # needs current column cell (rr) free in mask_cur
                        if (new_mask_cur >> rr) & 1:
                            ok = False
                            break
                        new_mask_cur |= (1 << rr)
                    else:
                        # needs next column cell (rr) free in next_mask
                        if (new_next_mask >> rr) & 1:
                            ok = False
                            break
                        new_next_mask |= (1 << rr)
                if ok:
                    dfs(new_mask_cur, new_next_mask)

        dfs(start_mask, 0)
        all_trans[start_mask] = sorted(results)
    return all_trans

TRANS = gen_transitions()

def count_tilings(n, mod=None):
    # dp over columns 0..n ; dp[c][mask] = ways
    dp = [0] * (1 << H)
    dp[0] = 1  # at column 0, nothing occupied
    for col in range(n):
        ndp = [0] * (1 << H)
        for mask in range(1 << H):
            ways = dp[mask]
            if ways == 0:
                continue
            for next_mask in TRANS[mask]:
                ndp[next_mask] += ways
                if mod:
                    ndp[next_mask] %= mod
        dp = ndp
    return dp[0] % mod if mod else dp[0]

# Examples
if __name__ == "__main__":
    for n in range(1, 11):
        print(f"n={n:2d} -> ways = {count_tilings(n)}")
