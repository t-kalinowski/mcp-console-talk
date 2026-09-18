group <- readline("Group to summarize: ")
d <- readr::read_csv("./measurements.csv",
                     show_col_types = FALSE)
values <- d$response[d$group == group]
print(summary(values))
