# Native Quarto rendering helpers. No server is launched during ordinary preview.
# In capture mode missing files are errors, never silently replaced by examples.
.console_mode <- as.character(params$output_source)
if (!.console_mode %in% c("r", "mcp")) {
  stop("output_source must be 'r' or 'mcp'", call. = FALSE)
}
source("examples/cells.R", local = TRUE)
.console_runtime <- new.env(parent = globalenv())
options(width = 62, digits = 7)

console_capture_text <- function(id) {
  path <- file.path("captures", paste0(id, ".txt"))
  if (!file.exists(path)) {
    stop("Missing capture: ", path,
         ". Run python examples/capture_console.py first, or use output_source:r.",
         call. = FALSE)
  }
  # readChar preserves final newlines and avoids inventing output separators.
  con <- file(path, open = "rb")
  on.exit(close(con))
  readChar(con, file.info(path)$size, useBytes = TRUE)
}

console_eval <- function(id) {
  source <- console_cells[[id]]
  if (is.null(source)) stop("Unknown R cell: ", id, call. = FALSE)
  for (expr in parse(text = source, keep.source = TRUE)) {
    value <- withVisible(eval(expr, envir = .console_runtime))
    if (value$visible) print(value$value)
  }
  invisible(NULL)
}

console_text <- function(id) {
  if (.console_mode == "mcp") {
    cat(console_capture_text(id))
  } else {
    console_eval(id)
  }
  invisible(NULL)
}

console_protocol <- function(id) {
  cat(console_capture_text(id))
  invisible(NULL)
}

console_source <- function(id, language) {
  cat("````", language, "\n", console_capture_text(paste0("excerpts/", id)),
      "\n````\n", sep = "")
  invisible(NULL)
}

console_plot <- function(id) {
  if (.console_mode == "mcp") {
    path <- file.path("captures", paste0(id, "-01.png"))
    if (!file.exists(path)) stop("Missing captured image: ", path, call. = FALSE)
    return(knitr::include_graphics(path))
  }
  if (id == "python-plot") {
    return(knitr::include_graphics("assets/python-scatter.png"))
  }
  console_eval(id)
}
