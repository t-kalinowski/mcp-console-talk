# Run from the presentation directory:
# Rscript examples/repository-development/plot.R examples/repository-development assets/repository-development
render_development <- function(data_dir, output_dir) {
  stopifnot(dir.exists(data_dir), length(output_dir) == 1L)
  library(ggplot2)
  library(dplyr)
  library(tidyr)
  library(patchwork)
  counts <- read.csv(file.path(data_dir, "repository-size.csv"), check.names = FALSE) |>
    mutate(time = as.POSIXct(committed_at, format = "%Y-%m-%dT%H:%M:%S", tz = "UTC"))
  prs <- read.csv(file.path(data_dir, "merged-prs.csv")) |>
    filter(base == "main") |>
    mutate(time = as.POSIXct(merged_at, format = "%Y-%m-%dT%H:%M:%S", tz = "UTC"))
  pr_categories <- read.csv(file.path(data_dir, "pr-categories.csv"))
  categories <- c("Core code", "Test code & fixtures", "Test transcripts", "Docs & examples", "Build & tooling")
  colors <- c("#2867A5", "#B56530", "#DFB28F", "#B59B35", "#84929B")
  names(colors) <- categories
  paper <- "#f7f7f2"
  ink <- "#18323f"
  muted <- "#65787e"
  last <- tail(counts, 1)
  stopifnot(nrow(counts) == 307L, nrow(prs) == 279L,
            all(rowSums(counts[categories]) == counts$total),
            all(counts$total > 0), all(diff(counts$time) >= 0),
            last$commit == "657a5981983768967deed83c070973848ec800fb")
  # Repeating the previous state at the next commit draws exact steps. Explicit
  # bounds preserve commits sharing a timestamp without stacking them together.
  steps <- bind_rows(lapply(seq_len(nrow(counts)), function(i) {
    current <- counts[i, c("time", categories, "total")]
    current$order <- i * 2L
    if (i == 1L) return(current)
    previous <- counts[i - 1L, c("time", categories, "total")]
    previous$time <- current$time
    previous$order <- i * 2L - 1L
    bind_rows(previous, current)
  }))
  bands <- steps |>
    pivot_longer(all_of(categories), names_to = "category", values_to = "lines") |>
    mutate(category = factor(category, levels = categories)) |>
    group_by(order) |>
    arrange(category, .by_group = TRUE) |>
    mutate(upper = cumsum(lines), lower = upper - lines,
           share = lines / total, upper_share = upper / total, lower_share = lower / total) |>
    ungroup() |>
    arrange(category, order)
  check <- bands |> group_by(order) |>
    summarise(total = sum(lines), top = max(upper), share = sum(share), .groups = "drop")
  stopifnot(all(check$total == steps$total), all(check$top == steps$total),
            all(abs(check$share - 1) < 1e-12))

  plot_theme <- theme_minimal(base_size = 17, base_family = "Arial") +
    theme(plot.background = element_rect(fill = paper, colour = NA),
          panel.grid.minor = element_blank(), panel.grid.major.x = element_blank(),
          panel.grid.major.y = element_line(colour = "#d8e0db", linewidth = .4),
          axis.text = element_text(colour = muted, size = 16),
          axis.title = element_text(colour = ink, size = 17),
          axis.title.y = element_text(margin = margin(r = 12)),
          axis.title.x = element_blank(),
          legend.position = "top", legend.justification = "left", legend.title = element_blank(),
          legend.text = element_text(size = 15, colour = ink),
          legend.key.width = grid::unit(16, "pt"),
          plot.margin = margin(8, 12, 8, 8))
  dates <- as.POSIXct(c("2026-07-27", "2026-08-10", "2026-08-24", "2026-09-07", "2026-09-18"), tz = "UTC")
  xscale <- function() scale_x_datetime(breaks = dates, date_labels = "%b %d", timezone = "UTC",
                                      limits = as.POSIXct(c("2026-07-27", "2026-09-20"), tz = "UTC"),
                                      expand = expansion(mult = 0))
  line_scale <- function() scale_y_continuous(breaks = seq(0, 150000, 25000),
    labels = scales::label_comma(), limits = c(0, 160000), expand = expansion(mult = 0))
  total <- ggplot(counts, aes(time, total)) +
    geom_step(direction = "hv", colour = colors[[1]], linewidth = 1.2) +
    geom_point(data = last, size = 3, colour = ink) +
    geom_text(data = last, aes(label = paste0(scales::comma(total), " lines")),
              nudge_x = -86400, nudge_y = 9500, hjust = 1, size = 6, colour = ink) +
    xscale() + line_scale() + labs(y = "Tracked text lines") + plot_theme
  latest_share <- as.numeric(last[1, categories]) / last$total
  labels <- setNames(paste0(categories, "  ", scales::percent(latest_share, accuracy = .1)), categories)
  legend <- function() scale_fill_manual(values = colors, breaks = categories,
                                          guide = guide_legend(nrow = 2, byrow = TRUE))
  absolute <- ggplot(bands) +
    geom_ribbon(aes(time, ymin = lower, ymax = upper, fill = category, group = category), stat = "identity") +
    geom_path(aes(time, upper, group = category), colour = paper, linewidth = .3) +
    geom_step(data = counts, aes(time, total), colour = ink, linewidth = .6) +
    xscale() + line_scale() + legend() + labs(y = "Tracked text lines") + plot_theme
  proportion <- ggplot(bands) +
    geom_ribbon(aes(time, ymin = lower_share, ymax = upper_share, fill = category, group = category), stat = "identity") +
    geom_path(aes(time, upper_share, group = category), colour = paper, linewidth = .3) +
    xscale() + scale_y_continuous(breaks = seq(0, 1, .25), labels = scales::label_percent(),
                                 limits = c(0, 1), expand = expansion(mult = 0)) +
    scale_fill_manual(values = colors, breaks = categories, labels = labels,
                      guide = guide_legend(nrow = 2, byrow = TRUE)) +
    labs(y = "Share of tracked text lines") + plot_theme

  milestones <- read.csv(file.path(data_dir, "feature-milestones.csv")) |>
    filter(number != 123L) |>
    mutate(time = as.POSIXct(mergedAt, format = "%Y-%m-%dT%H:%M:%S", tz = "UTC"),
           label = c("Python cells\nAug 3 · #24", "SQL / DuckDB\nAug 4 · #36",
                     "On-demand packages\nAug 24 · #123/124", "Sandboxed Linux\nSep 9 · #262",
                     "Docker targets\nSep 12 · #302"),
           label_time = as.POSIXct(c("2026-08-01", "2026-08-09", "2026-08-24", "2026-09-06", "2026-09-15"), tz = "UTC"),
           height = c(.80, .35, .80, .80, .35))
  stopifnot(identical(milestones$number, c(24L, 36L, 124L, 262L, 302L)))
  milestone_band <- ggplot(milestones) +
    geom_segment(aes(x = time, xend = label_time, y = 0, yend = height - .13), colour = muted, linewidth = .5) +
    geom_point(aes(time, 0), colour = "#167d76", size = 2.8) +
    geom_text(aes(label_time, height, label = label), colour = ink, size = 5.1, lineheight = 1.08) +
    xscale() + scale_y_continuous(limits = c(-.08, 1.03), expand = expansion(mult = 0)) +
    plot_theme + theme(axis.text = element_blank(), axis.title = element_blank(),
                        axis.title.y = element_blank(), panel.grid = element_blank(),
                        panel.grid.major.y = element_blank(), plot.margin = margin(4, 12, 0, 8))
  dots <- ggplot(prs, aes(time, changed)) +
    geom_vline(data = milestones, aes(xintercept = time), colour = "#c9d5cd", linewidth = .4) +
    geom_point(colour = "#2867A5", alpha = .6, size = 2.6) +
    geom_point(data = prs |> filter(number %in% milestones$number),
                shape = 21, fill = "#167d76", colour = ink, size = 3.2, stroke = .6) +
    xscale() + scale_y_log10(breaks = c(1, 10, 100, 1000, 10000), labels = scales::label_comma(),
                            limits = c(1, 50000)) +
    labs(y = "Lines changed · log scale") + plot_theme
  timeline <- milestone_band / dots + plot_layout(heights = c(1.25, 3.4))

  largest <- prs |> slice_max(changed, n = 6, with_ties = FALSE) |> arrange(desc(changed)) |>
    mutate(label = c("#197  Reorganize Python tests", "#258  Separate test contracts",
                     "#202  Simplify transcript support", "#266  Delegate sandbox supervision",
                     "#302  Docker execution targets", "#205  Simplify CLI tests"),
           label = factor(label, levels = rev(label)))
  stopifnot(identical(largest$number, c(197L, 258L, 202L, 266L, 302L, 205L)))
  large_parts <- pr_categories |> inner_join(largest[c("number", "label")], by = "number") |>
    mutate(category = factor(category, levels = categories))
  largest_plot <- ggplot(large_parts, aes(changed, label, fill = category)) +
    geom_col(width = .6, position = position_stack(reverse = TRUE)) +
    geom_text(data = largest, aes(changed + 500, label, label = scales::comma(changed)),
                inherit.aes = FALSE, hjust = 0, colour = ink, size = 5) +
    scale_x_continuous(breaks = seq(0, 40000, 10000), labels = scales::label_comma(),
                       limits = c(0, 42500), expand = expansion(mult = 0)) +
    labs(x = "Lines added + deleted", y = NULL) + legend() + plot_theme +
    theme(panel.grid.major.y = element_blank(), panel.grid.major.x = element_line(colour = "#d8e0db"),
          axis.title.x = element_text(colour = ink, size = 17, margin = margin(t = 8)))
  plots <- list(pr_timeline = timeline, repository_total = total,
                repository_categories = absolute, repository_proportions = proportion,
                largest_prs = largest_plot)
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  for (name in names(plots)) {
    ggsave(file.path(output_dir, paste0(name, ".svg")), plots[[name]],
           width = 14.8, height = 5.6, device = svglite::svglite, bg = paper)
  }
  write.csv(data.frame(category = categories, lines = as.numeric(last[1, categories]), share = latest_share),
            file.path(output_dir, "latest-shares.csv"), row.names = FALSE)
  list(plots = plots, counts = counts, bands = bands, prs = prs, output_dir = output_dir)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  stopifnot(length(args) == 2L)
  invisible(render_development(args[[1]], args[[2]]))
}
