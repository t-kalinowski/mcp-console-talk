# Generated from examples/cells.json.
console_cells <- list(
  "fit" = "d <- read.csv(\"examples/measurements.csv\")\nfit <- lm(response ~ temperature + group,\n          data = d)\nfit",
  "predict" = "head(predict(fit, d), 3)",
  "coefficients" = "coef(fit)",
  "r-plot" = "plot(d$temperature, d$response,\n     xlab = \"Temperature\",\n     ylab = \"Response\")",
  "progress" = "for (i in 1:20) {\n  cat(sprintf(\"\\rfit [%s%s] %3d%%\",\n      strrep(\"=\", i), strrep(\" \", 20 - i), i * 5))\n  flush.console()\n  Sys.sleep(0.15)\n}\ncat(\"\\n\")",
  "compact" = "cat(\"download 0%\\rdownload 50%\\rdownload 100%\\n\")",
  "error" = "checkpoint <- 42\nstop(\"inspect me\")",
  "checkpoint" = "checkpoint",
  "prompt" = "name <- readline(\"name> \")\nname",
  "browser-start" = "inspect_mean <- function(x) {\n  browser()\n  mean(x)\n}\n\ninspect_mean(c(1, 2, 3))",
  "requirements" = "library(data.table)\nlibrary(dtplyr)\npackageVersion(\"data.table\")",
  "flood" = "for (i in seq_len(10000)) {\n  cat(sprintf(\"row %05d\\n\", i))\n}\ncat(\"fit complete\\n\")"
)
