# Generated from examples/cells.json.
console_cells <- list(
  "fit" = "  d <- read.csv(\"examples/measurements.csv\")\n  fit <- lm(response ~ temperature + group,\n            data = d)\n  fit",
  "predict" = "head(predict(fit, d), 3)",
  "coefficients" = "coef(fit)",
  "r-plot" = "  plot(d$temperature, d$response,\n       xlab = \"Temperature\",\n       ylab = \"Response\")",
  "progress" = "  pb <- txtProgressBar(max = 20, style = 3, width = 20)\n  for (i in 1:20) {\n    Sys.sleep(0.15)\n    setTxtProgressBar(pb, i)\n  }\n  close(pb)",
  "compact" = "cat(\"download 0%\\rdownload 50%\\rdownload 100%\\n\")",
  "error" = "  checkpoint <- 42\n  stop(\"inspect me\")",
  "checkpoint" = "checkpoint",
  "prompt" = "  name <- readline(\"name> \")\n  name",
  "browser-start" = "  inspect_mean <- function(x) {\n    browser()\n    mean(x)\n  }\n\n  inspect_mean(c(1, 2, 3))",
  "requirements" = "  library(data.table)\n  library(dtplyr)\n  packageVersion(\"data.table\")",
  "flood" = "  for (i in seq_len(10000)) {\n    cat(sprintf(\"row %05d\\n\", i))\n  }\n  cat(\"fit complete\\n\")",
  "r-fork" = "  emit <- inline::cfunction(\n    body = 'write(1, \"native output\\\\n\", 14);\n            return R_NilValue;',\n    includes = \"#include <unistd.h>\"\n  )\n  job <- parallel::mcparallel(emit())\n  invisible(parallel::mccollect(job))",
  "r-fork-cat" = "  job <- parallel::mcparallel({\n    out <- pipe(\"cat\", \"w\")\n    cat(\"hello from fork\\n\", file = out)\n    close(out)\n  })\n  invisible(parallel::mccollect(job))"
)
