FROM rocker/tidyverse
ENV UV_INSTALL_DIR=/usr/local/bin
ENV UV_TOOL_BIN_DIR=/usr/local/bin
ENV RIG_PREFIX=/usr/local
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl -LsSf https://r-lib.github.io/rig/install.sh | sh
RUN uv tool install r-lib-ir
WORKDIR /workspace
