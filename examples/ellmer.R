# Run from this examples directory with ellmer and mcp.console installed.
# The currently documented source installation is:
# pak::pak("github::t-kalinowski/mcp-console/r")
# Presentation-day public installation: install.packages("mcp.console")
library(ellmer)
library(mcp.console)

chat <- chat_openai()
chat$register_tool(console_tool())
chat$chat(
  "Use Console to analyze measurements.csv, compare groups, and inspect a plot. The data are synthetic."
)
