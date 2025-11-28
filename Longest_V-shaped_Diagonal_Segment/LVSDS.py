def longest_v_shape(mat):
    R, C = len(mat), len(mat[0])
    dirs = [(1,1),(1,-1),(-1,1),(-1,-1)]
    
    # dp[i][j][d][b]
    # d = direction 0..3
    # b = 0(no bend), 1(bend used)
    dp = [[[[1 for _ in range(2)] for _ in range(4)] for _ in range(C)] for _ in range(R)]

    best = 1

    for i in range(R):
        for j in range(C):
            for d, (dx, dy) in enumerate(dirs):
                
                # extend same direction without bending
                px, py = i - dx, j - dy
                if 0 <= px < R and 0 <= py < C:
                    dp[i][j][d][0] = dp[px][py][d][0] + 1

                # extend after bending
                if 0 <= px < R and 0 <= py < C:
                    dp[i][j][d][1] = dp[px][py][d][1] + 1

                # try bending at current cell (switching direction ONCE)
                for od in range(4):
                    if od != d:
                        dp[i][j][d][1] = max(dp[i][j][d][1], dp[i][j][od][0])

                best = max(best, dp[i][j][d][0], dp[i][j][d][1])

    return best

mat = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Longest V-shaped diagonal =", longest_v_shape(mat))
