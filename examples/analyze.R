group <- readline("Group to summarize: ")
d <- read.csv("./measurements.csv")
values <- d$response[d$group == group]
print(summary(values))
