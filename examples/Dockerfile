FROM rocker/r-ver:4.6.1
RUN /rocker_scripts/install_python.sh
ENV PATH="/opt/venv/bin:${PATH}"
ENV RETICULATE_PYTHON=/opt/venv/bin/python
RUN apt-get update && apt-get install -y \
    --no-install-recommends libcap2 cmake \
    libssl-dev libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN LIBARROW_BINARY=true ARROW_DATASET=ON \
    install2.r --error --skipinstalled \
    reticulate DBI jsonlite png nanoarrow \
    duckdb arrow pillar tibble utf8
RUN pip install mcp-console==0.0.4 \
    numpy pandas matplotlib duckdb scikit-learn
WORKDIR /workspace
