# Use a standard base image
FROM debian:bullseye-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install common dependencies needed for testing, linting, etc.
# For example: Node.js, Python, git, and curl
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip \
    nodejs \
    npm \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# (Optional) Install a specific linter or tool
RUN npm install -g eslint

# Set a working directory
WORKDIR /app

# Verify installations
CMD ["echo", "Base image ready! Python version:", $(python3 --version), "Node version:", $(node --version)]

