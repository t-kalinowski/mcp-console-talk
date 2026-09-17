# Synthetic demo. Long work is deliberately slowed to expose polling.
set.seed(16)
B <- 100L
boot <- numeric(B)
for (i in seq_len(B)) {
  rows <- sample.int(nrow(d), replace = TRUE)
  boot[i] <- coef(lm(response ~ temperature + group, d[rows, ]))[["temperature"]]
  if (i %% 20L == 0L) cat("completed", i, "of", B, "\n")
  Sys.sleep(0.05)
}
quantile(boot, c(0.025, 0.975))
