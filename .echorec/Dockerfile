# Echorec run image for this sample repository (spec §9): devcontainer-compatible, non-root.
# .devcontainer/devcontainer.json builds from this file, so a developer gets the same toolchain.
FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends git ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ARG USERNAME=echorec
ARG UID=1000
RUN useradd --create-home --uid ${UID} --shell /bin/bash ${USERNAME} \
 && mkdir /workspace && chown ${USERNAME}:${USERNAME} /workspace

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install --no-cache-dir -r /tmp/requirements-dev.txt

ENV PYTHONPATH=/workspace/src
USER ${USERNAME}
WORKDIR /workspace
# Commands: tests: pytest -q; lint: ruff check . && ruff format --check .; security scan: bandit -q -r src; regression: pytest -q regression
CMD ["bash"]
