public class DATT {

    public static long countTilings(int n, long mod) {

        if (n == 1) return 1;
        if (n == 2) return 2;
        if (n == 3) return 5;

        long[] dp = new long[n + 1];
        dp[1] = 1;
        dp[2] = 2;
        dp[3] = 5;

        for (int i = 4; i <= n; i++) {
            dp[i] = (2 * dp[i - 1] + dp[i - 3]) % mod;
        }

        return dp[n];
    }

    public static void main(String[] args) {
        System.out.println(countTilings(10, 1_000_000_007)); // → 1255
    }
}
