d <- read.csv("examples/measurements.csv")
group <- readline("Group to summarize: ")
values <- d$response[d$group == group]
print(summary(values))
