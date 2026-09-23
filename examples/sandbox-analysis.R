d <- read.csv("examples/measurements.csv")
fit <- lm(response ~ temperature + group, data = d)
print(coef(fit))
