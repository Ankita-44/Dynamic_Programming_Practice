public class LVSDS {

    static int[][] DIR = {{1,1},{1,-1},{-1,1},{-1,-1}};

    public static int longestVShape(int[][] mat) {
        int R = mat.length, C = mat[0].length;

        int dp[][][][] = new int[R][C][4][2];
        int best = 1;

        // initialize all dp states to 1
        for (int i=0;i<R;i++)
            for (int j=0;j<C;j++)
                for (int d=0;d<4;d++)
                    dp[i][j][d][0] = dp[i][j][d][1] = 1;

        for (int i=0;i<R;i++) {
            for (int j=0;j<C;j++) {
                for (int d=0; d<4; d++) {

                    int dx = DIR[d][0], dy = DIR[d][1];
                    int px = i - dx, py = j - dy;

                    // continue straight (no bend)
                    if (px>=0 && py>=0 && px<R && py<C)
                        dp[i][j][d][0] = dp[px][py][d][0] + 1;

                    // continue straight after bend already happened
                    if (px>=0 && py>=0 && px<R && py<C)
                        dp[i][j][d][1] = Math.max(dp[i][j][d][1], dp[px][py][d][1] + 1);

                    // apply bend exactly once
                    for (int od=0; od<4; od++)
                        if (od != d)
                            dp[i][j][d][1] = Math.max(dp[i][j][d][1], dp[i][j][od][0]);

                    best = Math.max(best, Math.max(dp[i][j][d][0], dp[i][j][d][1]));
                }
            }
        }
        return best;
    }

    public static void main(String[] args) {
        int[][] mat = {
            {1,2,3},
            {4,5,6},
            {7,8,9}
        };

        System.out.println("Longest V-shaped diagonal = " + longestVShape(mat));
    }
}
